from __future__ import annotations
import asyncio
import asyncpg
from pathlib import Path
from argparse import ArgumentParser

from src.utils.logger import Logger
from src.utils.env import ENV, CONFIG
from src.utils.constants import BOTNAME

"""
Execute this in your psql terminal to create the migrations table:
CREATE TABLE IF NOT EXISTS migrations (
    name TEXT PRIMARY KEY
);
"""


class Database:
    """
    Database class to handle the connection to the database.

    Attributes
    ----------
    _dsn : str
        The database DSN.
    _logger : Logger
        The logger instance.
    _pool : asyncpg.Pool
        The connection pool to the database.
    """

    _dsn = ENV.databaseDSN
    _logger = Logger(f"{BOTNAME}.Database")
    _pool: asyncpg.Pool[asyncpg.Record] | None = None

    async def connect(self) -> None:
        """
        Connect to the database.

        Raises
        ------
        Exception
            If the connection to the database fails.

        Notes
        -----
        If the environment is set to "dev", the error message will be logged.
        If the environment is set to "prod", the error message will not be logged.

        If the connection fails, it will retry 3 times before raising the error.
        """
        self._logger.info("Connecting to the database...")
        retries = 0
        try:
            self._pool = await asyncpg.create_pool(dsn=self._dsn)
            self._logger.info("Connected to the database!")
        except Exception as e:
            if CONFIG.env == "dev":
                self._logger.error(f"Failed to connect to the database: {e}")
            else:
                if retries == 3:
                    self._logger.error("Failed to connect to the database!")
                    raise e
                self._logger.info("Retrying in 5 seconds...")
                await asyncio.sleep(5)
                await self.connect()
                retries += 1

    async def close(self) -> None:
        """
        Close the connection to the database.

        Notes
        -----
        If the connection is already closed, it will log a message saying so.
        """
        if self.isConnected:
            await (await self.pool).close()
            self._logger.info("Closed the database connection!")
        else:
            self._logger.info("Connection already closed!")

    @property
    def isConnected(self) -> bool:
        """
        Check if the connection to the database is still open.

        Returns
        -------
        bool
            Whether the connection is still open or not.
        """
        return self._pool is not None and not self._pool.is_closing()

    @property
    async def pool(self) -> asyncpg.Pool[asyncpg.Record]:
        """
        Get a connection to the database.

        Returns
        -------
        Connection
            A connection to the database.
        """
        if not self.isConnected:
            await self.connect()
        return self._pool  # type: ignore


def getUpAndDown(file: Path) -> tuple[str, str]:
    """
    Get the up and down SQL queries from a migration file.

    Parameters
    ----------
    file : pathlib.Path
        The migration file.

    Returns
    -------
    tuple[str, str]
        The up and down SQL queries
    """
    content = file.read_text()
    up, down = content.split("-- DOWN")
    return up, down


class Migrations:
    """
    Migrations class to handle the migrations of the database.

    Parameters
    ----------
    folder : pathlib.Path
        The folder containing the migration files.
    pool : asyncpg.Pool
        The connection pool to the database.
    """

    def __init__(self, folder: Path, pool: asyncpg.Pool):
        self._folder = folder
        self._logger = Logger(f"{BOTNAME}.Migrations")
        self._pool = pool

    async def apply(self, name: str) -> None:
        """
        Apply a migration.

        Parameters
        ----------
        name : str
            The name of the migration.

        Notes
        -----
        If the migration is not found, it will log an error message.
        If the migration is already applied, it will log an error message.
        If the migration is applied successfully, it will log a success message.
        """
        self._logger.info(f"Applying migration: {name}")
        file = self._folder / f"{name}.sql"

        if not file.exists():
            self._logger.error(f"Migration not found: {name}")

        up, down = getUpAndDown(file)
        try:
            async with self._pool.acquire() as conn:
                if await conn.fetchval(
                    "SELECT name FROM migrations WHERE name = $1", name
                ):
                    self._logger.error(f"Migration already applied: {name}")
                    return

                async with conn.transaction():
                    await conn.execute(up)
                    await conn.execute(
                        "INSERT INTO migrations (name) VALUES ($1)", name
                    )
            self._logger.info(f"Migration applied: {name}")
        except Exception as e:
            self._logger.error(f"Failed to apply migration: {name} - {e}")

    async def rollback(self, name: str) -> None:
        """
        Rollback a migration.

        Parameters
        ----------
        name : str
            The name of the migration.

        Notes
        -----
        If the migration is not found, it will log an error message.
        If the migration is not applied, it will log an error message.
        If the migration is rolled back successfully, it will log a success message.
        """
        self._logger.info(f"Rolling back migration: {name}")
        file = self._folder / f"{name}.sql"

        if not file.exists():
            self._logger.error(f"Migration not found: {name}")

        up, down = getUpAndDown(file)
        try:
            async with self._pool.acquire() as conn:
                if not await conn.fetchval(
                    "SELECT name FROM migrations WHERE name = $1", name
                ):
                    self._logger.error(f"Migration not applied: {name}")
                    return

                async with conn.transaction():
                    await conn.execute(down)
                    await conn.execute("DELETE FROM migrations WHERE name = $1", name)
            self._logger.info(f"Migration rolled back: {name}")
        except Exception as e:
            self._logger.error(f"Failed to rollback migration: {name} - {e}")

    async def applyAll(self) -> None:
        """
        Apply all migrations.

        Notes
        -----
        It will apply all the migrations in the folder.
        """
        files = self._folder.iterdir()
        for file in sorted(files):
            if file.suffix == ".sql":
                await self.apply(file.stem)

    async def rollbackAll(self) -> None:
        """
        Rollback all migrations.

        Notes
        -----
        It will rollback all the migrations in the folder.
        """
        for file in self._folder.iterdir():
            if file.suffix == ".sql":
                await self.rollback(file.stem)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "action", choices=["apply", "rollback", "apply-all", "rollback-all"]
    )
    parser.add_argument("name", nargs="?")
    args = parser.parse_args()

    db = Database()

    async def main():
        await db.connect()
        migrations = Migrations(
            Path(__file__).parent.parent.parent / "migrations", await db.pool
        )
        if args.action == "apply":
            await migrations.apply(args.name)
        elif args.action == "rollback":
            await migrations.rollback(args.name)
        elif args.action == "apply-all":
            await migrations.applyAll()
        elif args.action == "rollback-all":
            await migrations.rollbackAll()
        await db.close()

    asyncio.run(main())

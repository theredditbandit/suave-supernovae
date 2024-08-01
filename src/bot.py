import typing as t
from pathlib import Path

import disnake
from disnake.ext import commands

from src.utils.constants import BOTNAME
from src.utils.logger import Logger
from src.utils.env import ENV, CONFIG
# from src.utils.db import Database


class Bot(commands.InteractionBot):
    """
    Custom bot class that extends disnake.ext.commands.InteractionBot to make it easier to work with.
    """

    def __init__(self) -> None:
        self.logger = Logger(f"{BOTNAME}.Bot", fileLogging=CONFIG.env == "prod")
        # self.db = Database()

        intents = disnake.Intents.default()
        intents.typing = True
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        intents.presences = True
        intents.moderation = True

        if CONFIG.env == "dev":
            self.logger.warn("Bot is running in development mode.")

        super().__init__(
            intents=intents,
            allowed_mentions=disnake.AllowedMentions(
                everyone=False, roles=False, users=True
            ),
            owner_id=CONFIG.ownerId,
            test_guilds=(
                (CONFIG.testGuild,) if CONFIG.env == "dev" and CONFIG.testGuild else []
            ),
            command_sync_flags=commands.CommandSyncFlags(sync_commands=True),
            reload=CONFIG.env == "dev",
        )

    async def start(self, *args: t.Any, **kwargs: t.Any) -> None:
        """
        Start the bot and load extensions

        Parameters
        ----------
        args : typing.Any
            Arguments to pass to the super class
        kwargs : typing.Any
            Keyword arguments to pass to the super class

        Returns
        -------
        None
        """
        self.logger.info("Loading extensions...")
        self.load_extensions(str((Path(__file__).parent / "extensions")))
        # await self.db.connect()
        self.logger.info("Starting bot...")
        await super().start(*args, **kwargs)

    async def close(self) -> None:
        """
        Stop the bot

        Returns
        -------
        None
        """
        self.logger.info("Closing bot...")
        # await self.db.close()
        return await super().close()

    def run(self, *args: t.Any, **kwargs: t.Any) -> None:
        """
        Run the bot with the specified token

        Parameters
        ----------
        args : typing.Any
            Arguments to pass to the super class
        kwargs : typing.Any
            Keyword arguments to pass to the super class

        Returns
        -------
        None
        """
        super().run(ENV.token, *args, **kwargs)

    async def on_ready(self) -> None:
        """
        Event that is called when the bot is ready

        Returns
        -------
        None
        """
        self.logger.info(f"Bot ready. Logged in as {self.user}")

    async def on_error(self, event_method: str, *args: t.Any, **kwargs: t.Any) -> None:
        """
        Event that is called when an error occurs

        Parameters
        ----------
        event_method : str
            The method that caused the error
        args : typing.Any
            Arguments passed to the method
        kwargs : typing.Any
            Keyword arguments passed to the method

        Returns
        -------
        None
        """
        self.logger.error(f"Error in {event_method}.", exc_info=True)
        await super().on_error(event_method, *args, **kwargs)

import typing as t
from pathlib import Path

import disnake
from disnake.ext import commands

from src.utils.constants import BOTNAME
from src.utils.logger import Logger
from src.utils.env import ENV


class Bot(commands.InteractionBot):
    def __init__(self) -> None:
        self.logger = Logger(f"{BOTNAME}.Bot", fileLogging=ENV.env == "prod")
        intents = disnake.Intents.default()
        intents.typing = True
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        intents.presences = True
        intents.moderation = True

        if ENV.env == "dev":
            self.logger.warn("Bot is running in development mode.")

        super().__init__(
            intents=intents,
            allowed_mentions=disnake.AllowedMentions(
                everyone=False, roles=False, users=True
            ),
            owner_id=ENV.ownerId,
            test_guilds=(
                (ENV.testGuild,) if ENV.env == "dev" and ENV.testGuild else []
            ),
            command_sync_flags=commands.CommandSyncFlags(sync_commands=True),
            reload=ENV.env == "dev",
        )

    async def start(self, *args: t.Any, **kwargs: t.Any) -> None:
        self.logger.info("Loading extensions...")
        self.load_extensions(str((Path(__file__).parent / "extensions")))

        self.logger.info("Starting bot...")
        await super().start(*args, **kwargs)

    async def close(self) -> None:
        self.logger.info("Closing bot...")
        return await super().close()

    def run(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().run(ENV.token, *args, **kwargs)

    async def on_ready(self) -> None:
        self.logger.info(f"Bot ready. Logged in as {self.user}")

    async def on_error(self, event_method: str, *args: t.Any, **kwargs: t.Any) -> None:
        self.logger.error(f"Error in {event_method}.", exc_info=True)
        await super().on_error(event_method, *args, **kwargs)

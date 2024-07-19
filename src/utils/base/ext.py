import typing as t

from disnake.ext import commands

from src.bot import Bot
from src.utils.logger import Logger
from src.utils.constants import BOTNAME


class Extension(commands.Cog):
    __slots__: tuple[str] = ("bot",)

    def __init__(self, bot: Bot, *args: t.Any, **kwargs: t.Any) -> None:
        self.bot = bot

        super().__init__(*args, **kwargs)

    @property
    def logger(self):
        return Logger(f"{BOTNAME}.extensions.{self.__class__.__name__}")

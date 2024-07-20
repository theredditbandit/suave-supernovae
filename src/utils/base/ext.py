import typing as t

from disnake.ext import commands

from src.bot import Bot
from src.utils.logger import Logger
from src.utils.constants import BOTNAME


class Extension(commands.Cog):
    """
    Base class for extensions

    Parameters
    ----------
    bot : Bot
        The bot instance
    args : typing.Any
        Positional arguments
    kwargs : typing.Any
        Keyword arguments
    """

    def __init__(self, bot: Bot, *args: t.Any, **kwargs: t.Any) -> None:
        self.bot = bot
        self.logger = Logger(f"{BOTNAME}.extensions.{self.__class__.__name__}")

        super().__init__(*args, **kwargs)

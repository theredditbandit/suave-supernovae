from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path
from os import getenv
import typing as t

__all__: tuple[str, ...] = ("ENV",)

load_dotenv(Path(__file__).parent.parent.parent / ".env.local")


@dataclass
class Env:
    """
    Dataclass to store environment variables

    Parameters
    ----------
    token : str
        The bot token
    testGuild : int | None
        The test guild id
    env : typing.Literal["dev", "prod"]
        The environment the bot is running in
    ownerId : int
        The bot owner's id
    """

    token: str
    testGuild: int | None
    env: t.Literal["dev", "prod"]
    ownerId: int


T = t.TypeVar("T")


def getOptionalKey(key: str, converter: type, default: T) -> T:
    """
    Get an optional key from the environment

    Parameters
    ----------
    key : str
        The key to get
    converter : type
        The type to convert the key to
    default : T
        The default value if the key is not found

    Returns
    -------
    T
        The value of the key
    """
    return converter(getenv(key, default))


def getRequiredKey(key: str, converter: type):
    """
    Get a required key from the environment

    Parameters
    ----------
    key : str
        The key to get
    converter : type
        The type to convert the key to

    Returns
    -------
    typing.Any
        The value of the key

    Raises
    ------
    ValueError
        If the key is not found
    """
    value = getenv(key)
    if value is None:
        raise ValueError(f"Missing required key: {key}")
    return converter(value)


def getEnv():
    """
    Get the environment variables

    Returns
    -------
    Env
        The environment variables
    """
    return Env(
        token=getRequiredKey("TOKEN", str),
        testGuild=getOptionalKey("TEST_GUILD", int, None),
        env=getOptionalKey("ENV", str, "dev"),
        ownerId=getRequiredKey("OWNER_ID", int),
    )


ENV = getEnv()

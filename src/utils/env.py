from dataclasses import dataclass
import json
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
    """

    token: str
    databaseDSN: str
    groq: str


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
        databaseDSN=getRequiredKey("DATABASE_DSN", str),
        groq=getRequiredKey("GROQ", str),
    )


@dataclass
class Config:
    """
    Dataclass to store bot configuration

    Parameters
    ----------
    testGuild : int | None
        The test guild id
    env : typing.Literal["dev", "prod"]
        The environment the bot is running in
    ownerId : int
        The bot owner's id
    """

    testGuild: int | None
    env: t.Literal["dev", "prod"]
    ownerId: int


CONFIG_PATh = Path(__file__).parent.parent / "config.json"


def getOptionalConfigKey(
    config: dict[str, str], key: str, converter: type, default: T
) -> T:
    """
    Get an optional key from the bot configuration

    Parameters
    ----------
    config : dict[str, str]
        The bot configuration
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
    return converter(config.get(key)) if key in config else default


def getRequiredConfigKey(config: dict[str, str], key: str, converter: type) -> t.Any:
    """
    Get a required key from the bot configuration

    Parameters
    ----------
    config : dict[str, str]
        The bot configuration
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
    value = config.get(key)
    if value is None:
        raise ValueError(f"Missing required key: {key}")
    return converter(value)


def getConfig() -> Config:
    """
    Get the bot configuration

    Returns
    -------
    Config
        The bot configuration
    """
    with open(CONFIG_PATh) as file:
        config = json.load(file)
    return Config(
        testGuild=getOptionalConfigKey(config, "testGuild", int, None),
        env=getRequiredConfigKey(config, "env", str),
        ownerId=getRequiredConfigKey(config, "ownerId", int),
    )


ENV = getEnv()
CONFIG = getConfig()

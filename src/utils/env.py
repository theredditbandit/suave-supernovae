from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path
from os import getenv
import typing as t

__all__: tuple = ("ENV",)

load_dotenv(Path(__file__).parent.parent.parent / ".env.local")


@dataclass
class Env:
    token: str
    testGuild: int | None
    env: t.Literal["dev", "prod"]
    ownerId: int


T = t.TypeVar("T")


def getOptionalKey(key: str, converter: type, default: T) -> T:
    return converter(getenv(key, default))


def getRequiredKey(key: str, converter: type):
    value = getenv(key)
    if value is None:
        raise ValueError(f"Missing required key: {key}")
    return converter(value)


def getEnv():
    return Env(
        token=getRequiredKey("TOKEN", str),
        testGuild=getOptionalKey("TEST_GUILD", int, None),
        env=getOptionalKey("ENV", str, "dev"),
        ownerId=getRequiredKey("OWNER_ID", int),
    )


ENV = getEnv()

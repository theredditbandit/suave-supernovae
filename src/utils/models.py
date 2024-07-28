from dataclasses import dataclass
import asyncpg


"""
Usage:

await DBMessage.insertOne(pool, Message(userId=1, content="Hello, World!"))

pool can be obtained from bot.db.pool
"""


@dataclass
class Message:
    userId: int
    content: str
    link: str


@dataclass
class DBMessage(Message):
    id: int
    createdAt: str


class MessageModel:
    @staticmethod
    async def insertOne(pool: asyncpg.Pool, data: Message) -> DBMessage:
        async with pool.acquire() as c:
            d = await c.fetchrow(
                "INSERT INTO message (userId, content, link) VALUES ($1, $2, $3) RETURNING *",
                data.userId,
                data.content,
                data.link,
            )
            if not d:
                raise Exception("Failed to add data")
            return DBMessage(**d)

    @staticmethod
    async def selectOne(pool: asyncpg.Pool, id: int) -> DBMessage:
        async with pool.acquire() as c:
            d = await c.fetchrow("SELECT * FROM message WHERE id = $1", id)
            if not d:
                raise Exception("Failed to select data")
            return DBMessage(**d)

    @staticmethod
    async def selectAll(pool: asyncpg.Pool) -> list[DBMessage]:
        async with pool.acquire() as c:
            d = await c.fetch("SELECT * FROM message")
            if not d:
                raise Exception("Failed to select data")
            return [DBMessage(**i) for i in d]

    @staticmethod
    async def deleteOne(pool: asyncpg.Pool, id: int) -> DBMessage:
        async with pool.acquire() as c:
            d = await c.fetchrow("DELETE FROM message WHERE id = $1 RETURNING *", id)
            if not d:
                raise Exception("Failed to delete data")
            return DBMessage(**d)

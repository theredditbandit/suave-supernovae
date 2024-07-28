import re
import disnake
import datetime
import typing as t


class Messages:
    """
    A class to handle messages
    """

    @staticmethod
    async def getMessages(
        channel: (
            disnake.PartialMessageable
            | disnake.TextChannel
            | disnake.Thread
            | disnake.VoiceChannel
            | disnake.StageChannel
        ),
        limit: int | None = 100,
        order: t.Literal["asc", "desc"] = "desc",
        pattern: re.Pattern | None = None,
        timeBefore: int | None = None,
    ) -> tuple[disnake.Message, ...]:
        """
        Get messages from a Messageable

        Parameters
        ----------
        channel : disnake.PartialMessageable | GuildMessageable
            The channel to get messages from
        limit : int, optional
            The number of messages to get, by default 100
        order : typing.Literal["asc", "desc"], optional
            The order of the messages, by default "desc"
        pattern : re.Pattern, optional
            The pattern to filter the messages, by default None
        timeBefore : int, optional
            The time before the message, by default 1 hour

        Returns
        -------
        tuple[disnake.Message, ...]
            The messages from the channel
        """
        offset: datetime.datetime | None = None
        if timeBefore is not None:
            offset = datetime.datetime.now() - datetime.timedelta(hours=timeBefore)

        messages = await channel.history(limit=limit, after=offset).flatten()
        if pattern is not None:

            def patternFilter(m: disnake.Message):
                return pattern.search(m.content) is not None

            messages = list(filter(patternFilter, messages))
        if order == "asc":
            messages = messages[::-1]
        return tuple(messages)

    @staticmethod
    async def getUserMessages(
        user: disnake.User | disnake.Member,
        order: t.Literal["asc", "desc"] = "desc",
        channel: (
            disnake.PartialMessageable
            | disnake.TextChannel
            | disnake.Thread
            | disnake.VoiceChannel
            | disnake.StageChannel
            | None
        ) = None,
        limit: int | None = 100,
        pattern: re.Pattern | None = None,
        timeBefore: int | None = None,
    ):
        """
        Get messages from a user

        Parameters
        ----------
        user : disnake.User | disnake.Member
            The user to get messages from
        order : typing.Literal["asc", "desc"], optional
            The order of the messages, by default "desc"
        channel : disnake.PartialMessageable | GuildMessageable | None, optional
            The channel to get messages from, by default None
        limit : int, optional
            The number of messages to get, by default 100
        pattern : re.Pattern, optional
            The pattern to filter the messages, by default None
        timeBefore : int, optional
            The time before the message, by default None

        Returns
        -------
        tuple[disnake.Message, ...]
            The messages from the user
        """
        offset: datetime.datetime | None = None
        if timeBefore is not None:
            offset = datetime.datetime.now() - datetime.timedelta(hours=timeBefore)

        if channel is None:
            messages = await user.history(limit=limit, after=offset).flatten()
        else:

            def userFilter(m: disnake.Message):
                return m.author.id == user.id

            messages = list(
                filter(
                    userFilter,
                    await channel.history(limit=limit, after=offset).flatten(),
                )
            )
        if pattern is not None:

            def patternFilter(m: disnake.Message):
                return pattern.search(m.content) is not None

            messages = list(filter(patternFilter, messages))
        if order == "asc":
            messages = messages[::-1]
        return tuple(messages)

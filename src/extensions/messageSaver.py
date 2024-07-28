import disnake
import typing as t
from disnake.ext import commands
from src.utils.base.ext import Extension
from src.views.messagesView import SavedMessagesView
from src.utils.models import MessageModel, Message, DBMessage
import asyncpg

if t.TYPE_CHECKING:
    from src.bot import Bot


class MessageSaverCog(Extension):
    @commands.message_command(name="Save Message")
    async def saveMessage(
        self, inter: disnake.ApplicationCommandInteraction, message: disnake.Message
    ) -> None:
        messageUrl: str = message.jump_url
        interactionUserId: int = inter.user.id
        message_content: str = message.content
        messageToBeAdded: Message = Message(
            interactionUserId, message_content, messageUrl
        )
        pool = await self.bot.db.pool
        await MessageModel.insertOne(pool, messageToBeAdded)

        await inter.response.send_message("Message Saved", ephemeral=True)

    @commands.user_command(name="See Saved Messages")
    async def viewMessages(
        self, inter: disnake.ApplicationCommandInteraction, user: disnake.User
    ) -> None:
        interactionUserId: int = inter.user.id
        pool: asyncpg.Pool[asyncpg.Record] = await self.bot.db.pool
        saved_messages: list[DBMessage] = await MessageModel.selectByUserID(
            pool, interactionUserId
        )
        saved_messages_view = SavedMessagesView(inter, user, saved_messages)
        await saved_messages_view.send()


def setup(bot: "Bot"):
    bot.add_cog(MessageSaverCog(bot))

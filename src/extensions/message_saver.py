import disnake
import typing as t
from disnake.ext import commands
from src.utils.base.ext import Extension
from src.views.messagesView import SavedMessagesView


if t.TYPE_CHECKING:
    from src.bot import Bot


class MessageSaverCog(Extension):
    @commands.message_command(name="Save Message")
    async def save_message(
        self, inter: disnake.ApplicationCommandInteraction, message: disnake.Message
    ) -> None:
        message_url: str = message.jump_url
        interaction_user_id: int = inter.user.id

        # Some Database commands will go here

        await inter.response.send_message(
            f"message url: {message_url}, user id: {interaction_user_id}"
        )

    @commands.user_command(name="See Saved Messages")
    async def view_messages(
        self, inter: disnake.ApplicationCommandInteraction, user: disnake.User
    ) -> None:
        saved_messages_view = SavedMessagesView(inter, user)
        await saved_messages_view.send()


def setup(bot: "Bot"):
    bot.add_cog(MessageSaverCog(bot))

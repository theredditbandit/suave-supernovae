from typing import List
import disnake
from disnake.ext import commands
import math
from src.utils.base.ext import Extension
from src.utils.base.embed import sendEmbed, createEmbed


class SavedMessagesView(disnake.ui.View):
    def __init__(self, inter: disnake.Interaction, user: disnake.User) -> None:
        self.messages_per_page: int = 4
        self.user: disnake.User = user

        # The data is placeholder now, it'll be data fetched from database
        self.data: List[str] = [f"item {n}" for n in range(10)]

        self.index: int = 1
        self.number_of_pages = math.ceil(len(self.data) / self.messages_per_page)
        self.interaction = inter
        super().__init__(timeout=180)

    def create_embed(self) -> disnake.Embed:
        items: List = self.data[
            (self.index - 1) * self.messages_per_page : self.index
            * self.messages_per_page
        ]
        description: str = ""

        for i, item in enumerate(items):
            description += f"{i}: {item}\n"

        embed: disnake.Embed = createEmbed(
            self.user, "Saved Messages", description=description
        )
        return embed

    def update_buttons(self) -> None:
        self.previous.disabled = True if self.index == 1 else False
        self.next.disabled = True if self.index == self.number_of_pages else False

    async def update(self, inter: disnake.Interaction):
        self.update_buttons()
        await inter.response.edit_message(embed=self.create_embed(), view=self)

    async def send(self) -> None:
        self.update_buttons()
        await sendEmbed(
            self.interaction,
            embed=self.create_embed(),
            first=True,
            view=self,
            ephemeral=True,
        )

    @disnake.ui.button(label="<", style=disnake.ButtonStyle.green)
    async def previous(
        self, button: disnake.ui.Button, inter: disnake.Interaction
    ) -> None:
        self.index -= 1
        await self.update(inter)

    @disnake.ui.button(label=">", style=disnake.ButtonStyle.green)
    async def next(self, button: disnake.ui.Button, inter: disnake.Interaction) -> None:
        self.index += 1
        await self.update(inter)


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


def setup(bot: commands.Bot):
    bot.add_cog(MessageSaverCog(bot))

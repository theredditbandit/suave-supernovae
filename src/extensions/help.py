import disnake
from disnake.ext import commands
import typing as t
if t.TYPE_CHECKING:
    from src.bot import Bot

class HelpCog(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.slash_command(name="help", description="Shows a help message describing commands")
    async def help(self, inter: disnake.ApplicationCommandInteraction):
        """Sends a help message with all available commands."""
        embed = disnake.Embed(title="Help", description="List of all commands", color=0x00ff00)

        for command in self.bot.slash_commands:
            embed.add_field(
                name=f"/{command.name}",
                value=command.description or "No description",
                inline=False,
            )

        await inter.response.send_message(embed=embed, ephemeral=True)

def setup(bot: "Bot"):
    bot.add_cog(HelpCog(bot))

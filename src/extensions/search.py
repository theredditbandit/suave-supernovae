import disnake
from disnake.ext import commands
import requests
import wikipediaapi
import os
import typing as t

if t.TYPE_CHECKING:
    from src.bot import Bot

# Specify a user agent string
user_agent = "MyBot/1.0 (https://example.com; myemail@example.com)"

# Initialize the Wikipedia API with the user agent
wiki_wiki = wikipediaapi.Wikipedia(language="en", user_agent=user_agent)


class SearchCog(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
   
    @commands.slash_command(description="Search Wikipedia and send the best result.")
    async def wikisearch(
        self, inter: disnake.ApplicationCommandInteraction, query: str
    ):
        """Search Wikipedia and send the best result."""
        await inter.response.defer(ephemeral=True)  # Acknowledge the interaction early

        page = wiki_wiki.page(query)
        if page.exists():
            title = page.title
            # Get the first 512 characters of the summary
            summary = page.summary[:512]
            url = page.fullurl
            embed = disnake.Embed(
                title=title, description=summary, color=0x00FF00, url=url
            )
            await inter.edit_original_message(embed=embed)
        else:
            await inter.edit_original_message(content="No Wikipedia page found.")


def setup(bot: "Bot"):
    bot.add_cog(SearchCog(bot))

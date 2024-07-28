import groq
import disnake
import typing as t
from disnake.ext import commands
from src.utils.base.ext import Extension
from src.utils.base.embed import createEmbed
from src.utils.messages import Messages
from src.utils.prompts import get_ask_prompt, ASK_SYSTEM_PROMPT
from src.utils.env import ENV, CONFIG
from src.utils.logger import Logger

if t.TYPE_CHECKING:
    from src.bot import Bot


class Ask(Extension):
    def __init__(self, bot: "Bot"):
        self.client = groq.Client(api_key=ENV.groq)
        self.logger = Logger("Ask", fileLogging=CONFIG.env == "prod")

    @commands.slash_command(
        name="ask",
        description="Answers a query based on the information present in the channel/thread",
    )
    async def ask(self, inter: disnake.ApplicationCommandInteraction, query: str):
        await inter.response.defer(ephemeral=True)
        thread_name = inter.channel
        msg = await Messages.getMessages(channel=thread_name, limit=4000, order="asc")
        context = "\n".join([f"{i.author} says {i.content}" for i in msg])
        completion = self.client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": ASK_SYSTEM_PROMPT},
                {"role": "user", "content": get_ask_prompt(context, query)},
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
        )

        sol = completion.choices[0].message.content

        embed = createEmbed(
            inter.user, title=f"`Answering Query {query}`", description=sol
        )

        # await sendEmbed(inter, embed, first=False)
        await inter.followup.send(embed=embed)


def setup(bot: "Bot"):
    bot.add_cog(Ask(bot))

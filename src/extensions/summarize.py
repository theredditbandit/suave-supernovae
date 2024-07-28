import groq
import disnake
import typing as t
from disnake.ext import commands
from src.utils.base.ext import Extension
from src.utils.base.embed import createEmbed, sendEmbed
from src.utils.messages import Messages
from src.utils.prompts import SYSTEM_PROMPT
from src.utils.env import ENV, CONFIG
from src.utils.logger import Logger

if t.TYPE_CHECKING:
    from src.bot import Bot


class Summarize(Extension):
    def __init__(self, bot: "Bot"):
        self.client = groq.Client(api_key=ENV.groq)
        self.logger = Logger("Summarize", fileLogging=CONFIG.env == "prod")

    @commands.slash_command(
        name="summarize", description="summarize the content in a thread/channel"
    )
    async def summary(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        thread_name = inter.channel
        msg = await Messages.getMessages(channel=thread_name, limit=100, order="asc")
        context = "\n".join([f"{i.author} says {i.content}" for i in msg])
        summary_prompt = f"""Please summarize the following discord conversation , following the guidelines provided in the system prompt. Here are the messages.
        {context}
        Provide a comprehensive summary that captures the essence of this conversation, highlighting key topics, decisions, and any important context. Your summary should be concise yet informative, allowing someone who hasn't read the original messages to understand the main points and outcomes of the discussion.
            """
        completion = self.client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": summary_prompt},
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
        )

        summary = completion.choices[0].message.content

        embed = createEmbed(
            inter.user, title=f"`{thread_name}` summary", description=summary
        )

        await sendEmbed(inter, embed, first=False)


def setup(bot: "Bot"):
    bot.add_cog(Summarize(bot))

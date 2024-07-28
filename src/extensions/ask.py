import disnake
import groq
import typing as t
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from disnake.ext import commands
from src.utils.base.embed import createEmbed, sendEmbed
from src.utils.base.ext import Extension
from src.utils.env import ENV, CONFIG
from src.utils.messages import Messages
from src.utils.logger import Logger

if t.TYPE_CHECKING:
    from src.bot import Bot

nltk.download("punkt")
nltk.download("stopwords")


class Ask(Extension):
    def __init__(self, bot: "Bot"):
        self.client = groq.Client(api_key=ENV.groq)
        self.msgHandler = Messages()
        self.logger = Logger("Summarize", fileLogging=CONFIG.env == "prod")

    @commands.slash_command(
        name="ask",
        description="ask a query that returns the highest rated document in a channel/thread",
    )
    async def summary(self, inter: disnake.ApplicationCommandInteraction, query: str):
        thread_name = inter.channel
        msg = await self.msgHandler.getMessages(
            channel=thread_name, limit=100, order="asc"
        )
        corpus = []
        for message in msg:
            corpus.append(message.content)
        corpus = [i for i in corpus if i]
        self.logger.info(f"messages indexed into corpus: {corpus}")
        retrieved_docs = self.retrieve_documents(query, corpus)
        response = self.generate_response(retrieved_docs)
        embed = createEmbed(
            inter.user, title=f'{thread_name} query for "{query}"', description=response
        )
        await sendEmbed(inter, embed, first=True)

    def retrieve_documents(self, query, corpus):
        stop_words = set(stopwords.words("english"))
        query_tokens = [
            word.lower()
            for word in word_tokenize(query)
            if word.isalnum() and word.lower() not in stop_words
        ]
        query_counter = Counter(query_tokens)
        scores = []
        for doc in corpus:
            doc_tokens = [
                word.lower()
                for word in word_tokenize(doc)
                if word.isalnum() and word.lower() not in stop_words
            ]
            doc_counter = Counter(doc_tokens)
            score = sum(
                query_counter[word] * doc_counter[word] for word in query_counter
            )
            scores.append((score, doc))
        scores.sort(reverse=True, key=lambda x: x[0])
        return scores

    def generate_response(self, retrieved_docs):
        if not retrieved_docs or retrieved_docs[0][0] == 0:
            return "Couldn't find any information related to your query."
        top_doc = retrieved_docs[0][1]
        response_template = "Here's some information, based on your query: {}"
        return response_template.format(top_doc)


def setup(bot: "Bot"):
    bot.add_cog(Ask(bot))

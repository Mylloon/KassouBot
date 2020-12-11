import discord
from discord.ext import commands

def setup(client):
    client.add_cog(Autopublish(client))

class Autopublish(commands.Cog):
    """Autopublish."""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 786897204816117771 and message.author.name == "GitHub" and message.author.bot:
            await message.publish()
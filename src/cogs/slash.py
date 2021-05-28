import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

def setup(client):
    client.add_cog(Slash(client))

class Slash(commands.Cog):
    """Slash commands test."""

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="test")
    async def _test(self, ctx: SlashContext):
        embed = discord.Embed(title="embed test")
        await ctx.send(content="test", embeds=[embed])

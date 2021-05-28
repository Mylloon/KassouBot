import discord
import time
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

def setup(client):
    client.add_cog(Slash(client))

class Slash(commands.Cog):
    """Slash commands test."""

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="pingSlash", description = "Affiche mon ping.")
    async def _pingSlash(self, ctx: SlashContext):
        now = int(round(time.time() * 1000))
        ping = now - int(round(ctx.message.created_at.timestamp() * 1000))
        embed = discord.Embed(description = 'Pinging...')
        message = await ctx.send(embed = embed)
        ping2 = int(round(time.time() * 1000)) - now
        await message.edit(embed = discord.Embed(color = discord.Colour.random(), description = f':hourglass: {round(self.client.latency * 1000)} ms\n\n:stopwatch: {ping2} ms\n\n:heartbeat: {ping} ms'))
        await ctx.message.add_reaction(emoji = '✅')

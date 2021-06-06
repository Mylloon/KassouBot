print("Chargement des extensions & librairie...", end = " ")

import discord
import re
import os
from discord_slash import SlashCommand
from discord.ext import commands
from utils.core import userOrNick, goodTimezone
from utils.reminder import Reminder
customPrefix = os.environ['PREFIX']
customTimezone = os.environ['TIMEZONE']

client = commands.Bot(command_prefix = customPrefix, case_insensitive = True, intents = discord.Intents.all())
slash = SlashCommand(client, sync_commands = True)

client.load_extension("cogs.help")
client.load_extension("cogs.utils")
client.load_extension("cogs.internet")
client.load_extension("cogs.music")
client.load_extension("cogs.games")
client.load_extension("cogs.fun")
client.load_extension("cogs.school")
client.load_extension("cogs.citation")
client.load_extension("cogs.confreriedukassoulait") # you can remove this cogs, only for my private guild
Reminder().creationTable()
print("Terminé !")

@client.event
async def on_connect():
    print(f"Connecté !")

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Activity(name = f"{customPrefix}help", type = discord.ActivityType.playing))
    print("Bot prêt.")

@client.event
async def on_command_error(ctx, error):
    if not ctx.invoked_with.startswith(customPrefix):
        print(error)
        await ctx.message.add_reaction(emoji = '❓')

@client.event
async def on_message(message):
    await client.process_commands(message)

    if message.author == client.user:
        return
    
    """informations concernant le bot lorsqu'il est mentionner"""
    if client.user.mention == message.content.replace("!",""):
        ctx = await client.get_context(message)
        prefix = await client.get_prefix(message)
        await ctx.send(f">>> Coucou !\nMon préfix est `{prefix}` et ma commande d'aide est `{prefix}help`")

print("Connexion à Discord...", end = " ")
client.run(os.environ['TOKEN_DISCORD'])

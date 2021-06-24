print("Chargement des extensions & librairie...", end = " ")

import discord
from os import environ, listdir
from discord_slash import SlashCommand
from discord.ext import commands
from utils.reminder import Reminder
customPrefix = environ['PREFIX']

client = commands.Bot(command_prefix = customPrefix, case_insensitive = True, intents = discord.Intents.all())
slash = SlashCommand(client, sync_commands = True)

for file in listdir("cogs"):
    if file.endswith(".py") and file.startswith("-") == False:
        client.load_extension(f"cogs.{file[:-3]}")
print("Terminé !")

@client.event
async def on_connect():
    print(f"Connecté !")

@client.event
async def on_disconnect():
    print(f"Déconnecté.")

@client.event
async def on_resumed():
    print(f"Reconnecté !")

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Activity(name = f"{customPrefix}help", type = discord.ActivityType.playing))
    Reminder().creationTable()
    print("Bot prêt.")

@client.event
async def on_command_error(ctx, error):
    if not ctx.invoked_with.startswith(customPrefix):
        print(error)
        if ctx.message:
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
client.run(environ['TOKEN_DISCORD'])

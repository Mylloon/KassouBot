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
    
    """citation"""
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
    httpsString = "https://"
    channelsString = "discord.com/channels/"
    for i in range(len(urls)):
        if urls[i].startswith(f"{httpsString}{channelsString}") or urls[i].startswith(f"{httpsString}ptb.{channelsString}") or urls[i].startswith(f"{httpsString}canary.{channelsString}"):
            link = urls[i]
            linkURL = link
            if link.startswith(f"{httpsString}{channelsString}"):
                link = f'000{link}'
            if link.startswith(f"{httpsString}ptb.{channelsString}"):
                link = link[1:]
            if link.startswith(f"{httpsString}canary.{channelsString}"):
                link = link[4:]
            if "@me" in urls[i]:
                return await message.channel.send("Je ne cite pas les messages privés.", delete_after = 5)
            try:
                if int(link[32:-38]) == message.guild.id:
                    msgID = await client.get_channel(int(link[51:-19])).fetch_message(int(link[70:]))
                    couleur = 0x2f3136
                    msgFiles = msgID.attachments
                    imageExtensions = ["jpg", "jpeg", "png", "webp", "gif"]
                    desc = msgID.content
                    if len(msgFiles) > 1:
                        listOfFiles = ""
                        for i in range(0, len(msgFiles)):
                            listOfFiles = f"{listOfFiles}, {msgFiles[i].filename}"
                        listOfFiles = listOfFiles[2:]
                        if len(msgID.content) > 0:
                            desc = f"{msgID.content}\n\nIl y a plusieurs fichiers dans ce message : {listOfFiles}"
                        else:
                            desc = f"Il y a plusieurs fichiers dans ce message : {listOfFiles}"
                    else:
                        if len(msgFiles) == 1:
                            if msgFiles[0].filename[-4:].split('.')[1] in imageExtensions:
                                if not len(msgID.content) > 0:
                                    desc = f"Une image jointe : {msgFiles[0].filename}"
                            else:
                                linkFile = msgFiles[0].url
                                if not len(msgID.content) > 0:
                                    desc = f"Un fichier joint : {msgFiles[0].filename}"
                    embed = discord.Embed(description = desc, colour = couleur)
                    auteur = "Auteur"
                    if message.author == msgID.author:
                        auteur = "Auteur & Citateur"
                    embed.add_field(name = auteur, value = msgID.author.mention, inline=True)
                    try:
                        if len(msgFiles) == 1:
                            if msgFiles[0].filename[-4:].split('.')[1] in imageExtensions:
                                embed.set_image(url=msgFiles[0].url)
                            else:
                                embed.add_field(name = "Fichier", value = f"[Lien]({linkFile})", inline=True)
                    except:
                        pass
                    embed.add_field(name = "Message", value = f"{msgID.channel.mention} - [Lien Message]({linkURL})", inline=True)
                    embed.set_author(name = "Citation", icon_url = msgID.author.avatar_url)
                    icon_url = message.author.avatar_url

                    date_1 = goodTimezone(msgID.created_at, 0, customTimezone)
                    edit = ""
                    if msgID.edited_at:
                        date_edit = goodTimezone(msgID.edited_at, 0, customTimezone)
                        edit = f" et modifié le {date_edit[0][8:]}/{date_edit[0][5:-3]}/{date_edit[0][:4]} à {date_edit[1]}"
                    messageDuBas = f"Posté le {date_1[0][8:]}/{date_1[0][5:-3]}/{date_1[0][:4]} à {date_1[1]}{edit}"

                    date_2 = goodTimezone(message.created_at, 0, customTimezone)
                    date_2 = f"{date_2[0][8:]}/{date_2[0][5:-3]}/{date_2[0][:4]} à {date_2[1]}"
                    
                    if auteur == "Auteur":
                        messageDuBas = messageDuBas + f"\nCité par {userOrNick(message.author)} le {date_2}"
                    embed.set_footer(icon_url = icon_url, text = messageDuBas)
                    if message.content == linkURL.replace(' ',''):
                        await message.channel.send(embed = embed)
                        await message.delete()
                    else:
                        await message.reply(embed = embed, mention_author = False)
            except Exception as e:
                e = str(e)
                if not "invalid literal for int() with base 10:" in e or not "404 Not Found (error code: 10008)" in e: # faute de frappe / message supprimé
                    print(e)

print("Connexion à Discord...", end = " ")
client.run(os.environ['TOKEN_DISCORD'])

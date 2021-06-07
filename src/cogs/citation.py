import discord
import re
import os
from discord.ext import commands
customTimezone = os.environ['TIMEZONE']
from utils.core import userOrNick
from utils.time import goodTimezone

def setup(client):
    client.add_cog(Citation(client))

class Citation(commands.Cog):
    """Gère le système de citation."""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
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
                        msgID = await self.client.get_channel(int(link[51:-19])).fetch_message(int(link[70:]))
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

                        date_1 = goodTimezone(msgID.created_at, customTimezone)
                        edit = ""
                        if msgID.edited_at:
                            date_edit = goodTimezone(msgID.edited_at, customTimezone)
                            edit = f" et modifié le {date_edit[0][8:]}/{date_edit[0][5:-3]}/{date_edit[0][:4]} à {date_edit[1]}"
                        messageDuBas = f"Posté le {date_1[0][8:]}/{date_1[0][5:-3]}/{date_1[0][:4]} à {date_1[1]}{edit}"

                        date_2 = goodTimezone(message.created_at, customTimezone)
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

import discord
import re
import os
from discord.ext import commands
from random import choice
from datetime import datetime
from pytz import timezone
customTimezone = os.environ['TIMEZONE']

def setup(client):
    client.add_cog(ConfrerieDuKassoulait(client))

class ConfrerieDuKassoulait(commands.Cog):
    """Unique pour le serveur Discord "La confrérie du Kassoulait"."""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.client.get_channel(742564480050790512)
        await channel.send("Le bot a bien démarré.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 441208120644075520: # Confrérie du Kassoulait
            if member.bot == True:
                role = discord.utils.get(member.guild.roles, name = "Bot")
            else:
                role = discord.utils.get(member.guild.roles, name = "Copain")
            await member.add_roles(role)
            try:
                await member.send(f"Coucou **{member.name}** sur {member.guild.name} ! 🥰\n\nTu as le rôle **{role}** 💖!")
            except:
                pass
            channel = self.client.get_channel(741639570172674120) # salons des arrivées
            switch = [
                f"Bienvenue, {member.mention}. On espère que tu as apporté de la pizza.",
                f"C'est un plaisir de te voir, {member.mention}.",
                f"{member.mention} vient juste d'arriver !",
                f"{member.mention} vient juste d'atterrir.",
                f"{member.mention} vient de se glisser dans le serveur.",
                f"{member.mention} a bondi dans le serveur.",
                f"Contents de te voir, {member.mention}.",
                f"{member.mention} est arrivé(e).",
                f"Tout le monde, accueillez comme il se doit {member.mention} !",
                f"Youhou, tu as réussi, {member.mention} !",
                f"{member.mention} a rejoint le groupe."
            ]
            message = await channel.send("...") # évite d'envoyer une notification
            await message.edit(content = choice(switch))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 441208120644075520: # Confrérie du Kassoulait
            channel = self.client.get_channel(741639570172674120) # salons des arrivées
            await channel.send(f"{member.mention} vient de quitter le serveur.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 644922358745792512: # Règles de la Confrérie du Kassoulait
            if payload.emoji.name == '✅':
                role = discord.utils.get(payload.member.guild.roles, name="règles-acceptés")
                await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 644922358745792512: # Règles de la Confrérie du Kassoulait
            if payload.emoji.name == '✅':
                guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                role = discord.utils.get(guild.roles, name="règles-acceptés")
                await member.remove_roles(role)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.guild.id == 441208120644075520: # Confrérie du Kassoulait
            prefix = await self.client.get_prefix(message)
            if not (
                message.content.startswith(f"{prefix}note") or
                message.content.startswith(f"{prefix}memo") or
                len(re.findall(".com/channels/", message.content)) != 0 or
                self.client.user.id is message.author.id
            ):
                user_suppressed = None

                async for entry in message.guild.audit_logs(limit=1):
                    if (datetime.now() - entry.created_at).seconds < 5 and str(entry.action) == 'AuditLogAction.message_delete':
                        user_suppressed = entry.user
                
                channel = self.client.get_channel(742588187456831659)
                embed = discord.Embed(description = f"{message.content}")

                embed.set_author(name = self.user_or_nick(message.author), icon_url = message.author.avatar_url)

                if not user_suppressed:
                    embed.set_footer(text = f"Channel: #{message.channel.name} | Date : {self.goodTimezone(message.created_at, 1)}\nSupprimé le {datetime.now(timezone(customTimezone)).strftime('%d/%m/%Y à %H:%M:%S')}")
                else:                
                    embed.set_footer(icon_url = user_suppressed.avatar_url, text = f"Channel: #{message.channel.name} | Date : {self.goodTimezone(message.created_at, 1)}\nSupprimé par {self.user_or_nick(user_suppressed)} le {datetime.now(timezone(customTimezone)).strftime('%d/%m/%Y à %H:%M:%S')}")
                
                await channel.send(embed = embed)
                # ne fonctionne pas quand un message a été supprimé avant que le bot ai démarré
                # info sur la personne qui a supprimé ne fonctionne pas si il a supprimé un message auparavant (les logs se rajoute a un log deja existant)

    def user_or_nick(user):
        if user.nick:
            return f"{user.nick} ({user.name}#{user.discriminator})"
        else:
            return f"{user.name}#{user.discriminator}"

    def goodTimezone(self, date, type):
        if type == 0:
            return str(timezone(customTimezone).fromutc(date))[:-13].replace('-', '/').split()
        elif type == 1:
            return str(timezone(customTimezone).fromutc(date))[:-13].replace('-', '/').replace(' ', ' à ')
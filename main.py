print("Connexion à Discord...")

import discord, re, pytz
from discord.ext import commands
from random import randint, choice
from datetime import datetime, timedelta
from pytz import timezone
from tokens import token_discord as token

client = commands.Bot(command_prefix = ".", case_insensitive = True, intents = discord.Intents.all())

print("Chargement des extensions & librairie...")
client.load_extension("cogs.help")
client.load_extension("cogs.utils")
client.load_extension("cogs.internet")
client.load_extension("cogs.music")
client.load_extension("cogs.games")
client.load_extension("cogs.fun")
client.load_extension("cogs.autopublish")

@client.event
async def on_connect():
    print(f"Connecté avec le token : {token}.")

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Activity(name = ".help", type = discord.ActivityType.playing))
    print("Bot prêt.")
    channel = client.get_channel(742564480050790512)
    await channel.send("Le bot a bien démarré.")

@client.event
async def on_member_join(member):
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
        channel = client.get_channel(741639570172674120) # salons des arrivées
        switch = {
            0: f"Bienvenue, {member.mention}. On espère que tu as apporté de la pizza.",
            1: f"C'est un plaisir de te voir, {member.mention}.",
            2: f"{member.mention} vient juste d'arriver !",
            3: f"{member.mention} vient juste d'atterrir.",
            4: f"{member.mention} vient de se glisser dans le serveur.",
            5: f"{member.mention} a bondi dans le serveur.",
            6: f"Contents de te voir, {member.mention}.",
            7: f"{member.mention} est arrivé(e).",
            8: f"Tout le monde, accueillez comme il se doit {member.mention} !",
            9: f"Youhou, tu as réussi, {member.mention} !",
            10: f"{member.mention} a rejoint le groupe.",
        }
        message = await channel.send("...") # évite d'envoyer une notification
        await message.edit(content = choice(switch))

@client.event
async def on_member_remove(member):
    if member.guild.id == 441208120644075520: # Confrérie du Kassoulait
        channel = client.get_channel(741639570172674120) # salons des arrivées
        await channel.send(f"{member.mention} vient de quitter le serveur.")

@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 644922358745792512: # Règles de la Confrérie du Kassoulait
        if payload.emoji.name == '✅':
            role = discord.utils.get(payload.member.guild.roles, name="règles-acceptés")
            await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 644922358745792512: # Règles de la Confrérie du Kassoulait
        if payload.emoji.name == '✅':
            guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            role = discord.utils.get(guild.roles, name="règles-acceptés")
            await member.remove_roles(role)

@client.event
async def on_command_error(ctx, error):
    if not ctx.invoked_with.startswith('.'):
        await ctx.message.add_reaction(emoji = '❓')
        print(error)

@client.event
async def on_message(message):
    await client.process_commands(message)


    if message.author == client.user:
        return
    
    if client.user.mention == message.content.replace("!",""):
        ctx = await client.get_context(message)
        prefix = await client.get_prefix(message)
        await ctx.send(f">>> Coucou !\nMon préfix est `{prefix}` et ma commande d'aide est `{prefix}help`")
    
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
    for i in range(len(urls)):
        if urls[i].startswith("https://discordapp.com/channels/") or urls[i].startswith("https://discord.com/channels/") or urls[i].startswith("https://ptb.discordapp.com/"):
            link = urls[i]
            linkURL = link
            if link.startswith("https://discord.com/channels/"):
                link = f'000{link}'
            if link.startswith("https://ptb.discordapp.com/"):
                link = link[4:]
            if "@me" in urls[i]:
                return await message.channel.send("Je ne cite pas les messages privés.", delete_after = 5)
            try:
                if int(link[32:-38]) == message.guild.id:
                    msgID = await client.get_channel(int(link[51:-19])).fetch_message(int(link[70:]))
                    couleur = 0x2f3136
                    if len(msgID.content) > 0:
                        embed = discord.Embed(description = msgID.content, colour = couleur)
                    else:
                        embed = discord.Embed(description = "Pas de message (image ? vidéo ? intégration ?)", colour = couleur) # peut etre implémenter autre chose
                    auteur = "Auteur"
                    if message.author == msgID.author:
                        auteur = "Auteur & Citateur"
                    embed.add_field(name = auteur, value = msgID.author.mention, inline=True)
                    embed.add_field(name = "Message", value = f"{msgID.channel.mention} - [Lien Message]({linkURL})", inline=True)
                    embed.set_author(name = "Citation", icon_url = msgID.author.avatar_url)

                    icon_url = message.author.avatar_url

                    date_1 = str(msgID.created_at.astimezone(timezone('Europe/Paris')))[:-13].replace('-', '/').split()
                    edit = ""
                    if msgID.edited_at:
                        date_edit = str(msgID.edited_at.astimezone(timezone('Europe/Paris')))[:-13].replace('-', '/').split()
                        edit = f"(Dernier edit : {date_edit[0][8:]}/{date_edit[0][5:-3]}/{date_edit[0][:4]} à {date_edit[1]})"
                    message_1 = f"Date : {date_1[0][8:]}/{date_1[0][5:-3]}/{date_1[0][:4]} à {date_1[1]} {edit}"

                    date_2 = str(message.created_at.astimezone(timezone('Europe/Paris')))[:-13].replace('-', '/').split()
                    date_2 = f"{date_2[0][8:]}/{date_2[0][5:-3]}/{date_2[0][:4]} à {date_2[1]}"
                    
                    cite = ""
                    if auteur == "Auteur":
                        cite = f"\nCité par {user_or_nick(message.author)} le {date_2}"
                    embed.set_footer(icon_url = icon_url, text = f"{message_1}{cite}")
                    await message.channel.send(embed = embed)
                    if message.content == linkURL.replace(' ',''):
                        await message.delete()
            except Exception as e:
                e = str(e)
                if not "invalid literal for int() with base 10:" in e or not "404 Not Found (error code: 10008)" in e: # faute de frappe / message supprimé
                    print(e)

@client.event
async def on_message_delete(message):
    if message.author.guild.id == 441208120644075520: # Confrérie du Kassoulait
        prefix = await client.get_prefix(message)
        if not (
            message.content.startswith(f"{prefix}note") or
            message.content.startswith(f"{prefix}memo") or
            len(re.findall(".com/channels/", message.content)) != 0 or
            client.user.id is message.author.id
        ):
            user_suppressed = None

            async for entry in message.guild.audit_logs(limit=1):
                if (datetime.now() - entry.created_at).seconds < 5 and str(entry.action) == 'AuditLogAction.message_delete':
                    user_suppressed = entry.user
            
            channel = client.get_channel(742588187456831659)
            embed = discord.Embed(description = f"{message.content}")

            embed.set_author(name = user_or_nick(message.author), icon_url = message.author.avatar_url)

            if not user_suppressed:
                embed.set_footer(text = f"Channel: #{message.channel.name} | Date : {str(message.created_at.astimezone(timezone('Europe/Paris')))[:-13].replace('-', '/').replace(' ', ' à ')}\nSupprimé le {datetime.now(pytz.timezone('Europe/Paris')).strftime('%d/%m/%Y à %H:%M:%S')}")
            else:                
                embed.set_footer(icon_url = user_suppressed.avatar_url, text = f"Channel: #{message.channel.name} | Date : {str(message.created_at.astimezone(timezone('Europe/Paris')))[:-13].replace('-', '/').replace(' ', ' à ')}\nSupprimé par {user_or_nick(user_suppressed)} le {datetime.now(pytz.timezone('Europe/Paris')).strftime('%d/%m/%Y à %H:%M:%S')}")
            
            await channel.send(embed = embed)
            # ne fonctionne pas quand un message a été supprimé avant que le bot ai démarré
            # info sur la personne qui a supprimé ne fonctionne pas si il a supprimé un message auparavant (les logs se rajoute a un log deja existant)

def user_or_nick(user):
    if user.nick:
        return f"{user.nick} ({user.name}#{user.discriminator})"
    else:
        return f"{user.name}#{user.discriminator}"

client.run(token)

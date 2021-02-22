import discord, pytz, time
from discord.ext import commands
from random import randint, shuffle
from datetime import datetime
from pytz import timezone
import re
import asyncio

def setup(client):
    client.add_cog(Utils(client))

class Utils(commands.Cog):
    """Commandes essentielles."""

    def __init__(self, client):
        self.client = client


    @commands.command(name='ping')
    async def _ping(self, ctx, *, question = '0'):
        """Affiche mon ping.⁢⁢⁢⁢⁢\n	➡ Syntaxe: .ping [help]⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        if question == 'help':
            return await ctx.send(embed = discord.Embed(color = randint(0, 0xFFFFFF), description = ":hourglass: correspond au temps entre deux battements de cœurs (en millisecondes)\n\n:stopwatch: correspond au temps que met le client a calculer le ping (en millisecondes)\n\n:heartbeat: correspond au temps que met le client a réagir au messages (en millisecondes)"))
        else:
            now = int(round(time.time() * 1000))
            ping = now - int(round(ctx.message.created_at.timestamp() * 1000))
            embed = discord.Embed(description = 'Pinging...')
            message = await ctx.send(embed = embed)
            ping2 = int(round(time.time() * 1000)) - now
            await message.edit(embed = discord.Embed(color = randint(0, 0xFFFFFF), description = f':hourglass: {round(self.client.latency * 1000)}ms\n\n:stopwatch: {ping2}ms\n\n:heartbeat: {ping}ms'))
            await ctx.message.add_reaction(emoji = '✅')

    @commands.command(name='avatar')
    async def _avatar(self, ctx, *, user = '0'):
        """Affiche ton avatar ou celui que tu mentionnes.\n	➡ Syntaxe: .avatar [user]"""
        if user == '0':
            user = ctx.author
        else:
            user = self.client.get_user(int(user[2:-1].replace("!","")))
        await ctx.message.add_reaction(emoji = '✅')
        embed = discord.Embed(description = f"[lien vers la photo de profil]({user.avatar_url}) de {user.mention}", color = randint(0, 0xFFFFFF))
        embed.set_author(name = f"Photo de profil de {user.name}")
        embed.set_image(url = user.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(name='calc')
    async def _calc(self, ctx, *, msg):
        """Calculatrice.\n	➡ Syntaxe: .calc <calcul>⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        equation = msg.replace('^', '**').replace('x', '*').replace('×', '*').replace('÷', '/').replace('≥', '>=').replace('≤', '<=')
        try:
            try:
                if '=' in equation:
                    if '<' in equation:
                        left = eval(equation.split("<=")[0])
                        right = eval(equation.split("<=")[1])
                        answer = str(left <= right)
                    elif '>' in equation:
                        left = eval(equation.split(">=")[0])
                        right = eval(equation.split(">=")[1])
                        answer = str(left >= right)
                    else:
                        left = eval(equation.split("=")[0])
                        right = eval(equation.split("=")[1])
                        answer = str(left == right)
                else:
                    answer = str(eval(equation))
            except ZeroDivisionError:
                return await ctx.send("Tu ne peux pas divisé par 0.")
        except TypeError:
            return await ctx.send("Requête de calcul invalide.")
        if '.' in answer:
            aftercomma = answer.split(".")[1]
            if len(aftercomma) > 2:
                answer = str(round(float(answer),2))
                equation = f"'{equation}' arrondi à 2"
        equation = equation.replace('*', '×').replace('/', '÷').replace('>=', '≥').replace('<=', '≤')
        embed = discord.Embed(color = randint(0, 0xFFFFFF), title = 'Calculatrice')
        embed.set_footer(text = ctx.author)

        embed.add_field(name = 'Calcul :', value = equation, inline = False)
        embed.add_field(name = 'Réponse :', value = answer.replace('False', 'Faux').replace('True', 'Vrai'), inline = False)
        await ctx.message.add_reaction(emoji = '✅')
        await ctx.send(content = None, embed = embed)
    @_calc.error
    async def _calc_error(self, ctx, error):
        await ctx.send("Tu n'as pas spécifié de calcul.")

    @commands.command(name='syntax')
    async def _syntax(self, ctx):
        """Informations pour bien éditer son texte.⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        syntaxe = "-----------------------------------------------------\n"
        syntaxe += discord.utils.escape_markdown("```Js\n")
        syntaxe += discord.utils.escape_markdown("//code en js (possible de remplacer 'js' par d'autres languages . adaptez le !)\n")
        syntaxe += discord.utils.escape_markdown('console.log("hi");\n')
        syntaxe += discord.utils.escape_markdown("```\n")
        syntaxe += "```Js\n"
        syntaxe += "//code en js (possible de remplacer 'js' par d'autres languages . adaptez le !)\n"
        syntaxe += 'console.log("hi");\n'
        syntaxe += "```\n"
        syntaxe += "Si ton code est trop long, mets le sur <https://pastebin.com/>\n"
        syntaxe += "-----------------------------------------------------\n"
        syntaxe += discord.utils.escape_markdown("`code sur une seule ligne`\n")
        syntaxe += "`code sur une seule ligne`\n"
        syntaxe += "-----------------------------------------------------\n"
        syntaxe += discord.utils.escape_markdown("*texte en italique*\n")
        syntaxe += "*texte en italique*\n"
        syntaxe += "-----------------------------------------------------\n"
        syntaxe += discord.utils.escape_markdown("**text en gras**\n")
        syntaxe += "**text en gras**\n"
        syntaxe += "-----------------------------------------------------\n"
        syntaxe += discord.utils.escape_markdown("<<https://www.youtube.com/watch?v=GhuYKL5NUYg>>\n")
        syntaxe += "Un lien entre crochet, ça empêche Discord de rajouté son intégration automatique (mais le lien fonctionnera toujours).\n"
        syntaxe += "-----------------------------------------------------\n"
        syntaxe += discord.utils.escape_markdown("__texte souligné__\n")
        syntaxe += "__texte souligné__\n"
        syntaxe += "-----------------------------------------------------\n"
        syntaxe += discord.utils.escape_markdown("~~texte barré~~\n")
        syntaxe += "~~texte barré~~\n"
        syntaxe += "-----------------------------------------------------\n"
        syntaxe += discord.utils.escape_markdown("~~__***text en italique-gras-souligné-barré***__~~\n")
        syntaxe += "~~__***text en italique-gras-souligné-barré***__~~\n"
        syntaxe += "-----------------------------------------------------\n"
        syntaxe += discord.utils.escape_markdown("\:joy: <- l'emoji ne va pas fonctionné grâce au \ \n")
        syntaxe += "\:joy: <- l'emoji ne va pas fonctionné grâce au \ \n"
        syntaxe += "-----------------------------------------------------\n"
        syntaxe += discord.utils.escape_markdown("> cette ligne est cité\npas celle là\n")
        syntaxe += "> cette ligne est cité\npas celle là\n"
        syntaxe += "-----------------------------------------------------\n"
        syntaxe += discord.utils.escape_markdown(">>> cette ligne est cité\ncelle là aussi (et elles le seront toutes!)\n")
        syntaxe += ">>> cette ligne est cité\ncelle là aussi (et elles le seront toutes!)\n"
        await ctx.message.add_reaction(emoji = '✅')
        await ctx.send(syntaxe)

    @commands.command(name='memo', aliases = ['note'])
    async def _memo(self, ctx, *, text):
        """T'envoie un petit memo par message privé.\n	➡ Syntaxe: .memo/note <message>⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        if len(text) <= 5:
            await ctx.message.add_reaction(emoji = '❌')
            return await ctx.send("Ta note doit au moins faire 5 caractères.")
        elif len(text) >= 2048:
            await ctx.message.add_reaction(emoji = '❌')
            return await ctx.send("Ta note doit faire moins de 2048 caractères.")
        else:
            await ctx.message.delete()
            embed = discord.Embed(description = text, color = randint(0, 0xFFFFFF))
            embed.set_author(name = f"Mémo noté depuis {ctx.guild.name}", icon_url = ctx.author.avatar_url)
            embed.set_footer(text = f'📝 le {datetime.now(pytz.timezone("Europe/Paris")).strftime("%d/%m/%Y à %H:%M:%S")}')
            await ctx.author.send(embed = embed)
            return await ctx.send("Tu viens de recevoir ton mémo !", delete_after = 5)
    @_memo.error
    async def _note_error(self, ctx, error):
        if str(error) == "text is a required argument that is missing.":
            await ctx.send("Vous devez renseigner un message : `.note/memo <message>⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢`.")

    @commands.command(name='infos', aliases = ['info'])
    async def _infos(self, ctx):
        """Donne des infos sur le bot.\n	➡ Syntaxe: .infos/info⁢"""
        appinfo = await self.client.application_info()

        embed = discord.Embed(color = randint(0, 0xFFFFFF))

        embed.set_author(name = appinfo.name, icon_url = self.client.user.avatar_url)

        total_online = len({m.id for m in self.client.get_all_members() if m.status is discord.Status.online})
        total_unique = len(self.client.users)

        voice_channels = []
        text_channels = []
        for guild in self.client.guilds:
            voice_channels.extend(guild.voice_channels)
            text_channels.extend(guild.text_channels)

        text = len(text_channels)
        voice = len(voice_channels)

        embed.add_field(name = "Dev", value = f"[{appinfo.owner}](https://github.com/Mylloon)")
        embed.add_field(name = "Serveurs", value = len(self.client.guilds))
        embed.add_field(name = "Membres", value = f"{total_unique} au total\n{total_online} en ligne")
        embed.add_field(name = "Channels", value = f"{text} textuelles\n{voice} vocales")
        embed.set_footer(text = f"Basé sur discord.py {discord.__version__}")
        await ctx.message.add_reaction(emoji = '✅')
        await ctx.send(embed = embed)

    def _map_list_among_us(self, map):
        maps = {}
        maps["skeld"] = ["skeld", "the skeld", "theskeld"]
        maps["mira"] = ["mira", "mira hq", "mirahq"]
        maps["polus"] = ["polus"]
        maps["airship"] = ["airship", "air ship"]
        if map == "all":
            return maps["skeld"] + maps["mira"] + maps["polus"] + maps["airship"]
        return maps[map]
    
    @commands.command(name='among', hidden = True)
    async def _among(self, ctx, *, args = ""):
        if not args == "":
            args = args.split()
            del args[0]
            args = " ".join(args)
            if args.lower() in self._map_list_among_us("all"):
                await ctx.invoke(self.client.get_command("amongus"), map=args)
            else:
                await ctx.invoke(self.client.get_command("amongus"))
        else:
            await ctx.message.add_reaction(emoji = '❓')

    @commands.command(name='amongus')
    async def _amongus(self, ctx, *, map = "0"):
        """Affiche la carte voulue d'Among Us.⁢⁢⁢⁢⁢\n	➡ Syntaxe: .amongus <carte>⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        if map.lower() in self._map_list_among_us("mira"):
            image = "https://i.imgur.com/6ijrH1h.jpg"
            embed = discord.Embed(title = f"Map Mira HQ d'Among Us", color = randint(0, 0xFFFFFF), description = f"[lien de l'image]({image})")
            embed.set_image(url = image)
            await ctx.send(embed = embed)
            await ctx.message.add_reaction(emoji = '✅')
        elif map.lower() in self._map_list_among_us("polus"):
            image = "https://i.imgur.com/mhFmcw3.jpg"
            embed = discord.Embed(title = f"Map Polus d'Among Us", color = randint(0, 0xFFFFFF), description = f"[lien de l'image]({image})")
            embed.set_image(url = image)
            await ctx.send(embed = embed)
            await ctx.message.add_reaction(emoji = '✅')
        elif map.lower() in self._map_list_among_us("skeld"):
            image = "https://i.imgur.com/OSXI4Zv.jpg"
            embed = discord.Embed(title = f"Map The Skeld d'Among Us", color = randint(0, 0xFFFFFF), description = f"[lien de l'image]({image})")
            embed.set_image(url = image)
            await ctx.send(embed = embed)
            await ctx.message.add_reaction(emoji = '✅')
        elif map.lower() in self._map_list_among_us("airship"):
            image = "https://i.imgur.com/CYbPlQ6.png"
            embed = discord.Embed(title = f"Map Airship d'Among Us", color = randint(0, 0xFFFFFF), description = f"[lien de l'image]({image})")
            embed.set_image(url = image)
            await ctx.send(embed = embed)
            await ctx.message.add_reaction(emoji = '✅')
        else:
            await ctx.send("`.amongus <mira/polus/skeld/airship>`")

    @commands.command(name='whois')
    async def _whois(self, ctx, *user: discord.Member):
        """Affiche les infos sur l'utilisateur.⁢⁢⁢⁢⁢\n	➡ Syntaxe: .whois [user]⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        if len(user) <= 1:
            if user == ():
                user = [ctx.author]
            nom = f"{user[0].name}#{user[0].discriminator}"
            if user[0].nick:
                nom = f"{user[0].nick} ({user[0].name}#{user[0].discriminator})"
            embed = discord.Embed(color = randint(0, 0xFFFFFF)).set_author(name = nom, icon_url = user[0].avatar_url)
            
            embed.add_field(name = "ID", value = user[0].id)
            
            value = str(user[0].created_at.astimezone(timezone('Europe/Paris')))[:-13].replace('-', '/').split()
            embed.add_field(name = "Compte créé le", value = f"{value[0][8:]}/{value[0][5:-3]}/{value[0][:4]} à {value[1]}")
            
            embed.add_field(name = "Âge du compte", value = self._age_layout(self._get_age(user[0].created_at)))
            
            embed.add_field(name = "Mention", value = user[0].mention)
            
            value = str(user[0].joined_at.astimezone(timezone('Europe/Paris')))[:-13].replace('-', '/').split()
            embed.add_field(name = "Serveur rejoint le", value = f"{value[0][8:]}/{value[0][5:-3]}/{value[0][:4]} à {value[1]}")
            
            embed.add_field(name = "Est sur le serveur depuis", value = self._age_layout(self._get_age(user[0].joined_at)))
            await ctx.message.add_reaction(emoji = '✅')
            return await ctx.send(embed = embed)
        await ctx.send("Tu mentionnes trop d'utilisateurs :  `.whois [@Membre]`")
    def _get_age(self, date):
        joursRestants = datetime.now() - date
        years = joursRestants.total_seconds() / (365.242 * 24 * 3600)
        months = (years - int(years)) * 12
        days = (months - int(months)) * (365.242 / 12)
        hours = (days - int(days)) * 24
        minutes = (hours - int(hours)) * 60
        seconds = (minutes - int(minutes)) * 60
        return (int(years), int(months), int(days),  int(hours), int(minutes), int(seconds))
    def _age_layout(self, tuple):
        time = {}
        time[0], time[1], time[2], time[3], time[4], time[5] = "an", "mois", "jour", "heure", "minute", "seconde"
        for i in range(len(tuple)):
            if tuple[i] > 1 and i != 1:
                time[i] = time[i] + "s"
        message = ""
        if tuple[5] > 0: # pour les secondes
            affichage = [5] # on affiche que : seconde
        if tuple[4] > 0:
            affichage = [4, 5] # on affiche : minute + seconde
        if tuple[3] > 0:
            affichage = [3, 4, 5] # on affiche : heure + minute + seconde
        if tuple[2] > 0:
            affichage = [2, 3, 4] # on affiche : jour + heure + minute
        if tuple[1] > 0:
            affichage = [1, 2, 3] # on affiche : mois + jour + heure
        if tuple[0] > 0:
            affichage = [0, 1, 3] # on affiche : an + mois + heure
        for i in affichage:
            message = message + f", {tuple[i]} {time[i]}"
        return message[2:]

    @commands.command(name='sondage')
    async def _sondage(self, ctx, *args):
        """Fais un sondage.⁢⁢⁢⁢⁢\n	➡ Syntaxe: .sondage "<Question>" "<Proposition1>" "<Proposition...>" "<Proposition20>" """
        args = list(args)
        if len(args) > 2:
            question = args[0].replace("<@!", "").replace(">", "").replace("<@", "")
            for i in re.findall(r'\d+', question):
                ii = self.user_or_nick(ctx.author.guild.get_member(int(i)))
                try:
                    question = question.replace(i, ii)
                except:
                    pass
            propositions = args[1:]
            if len(propositions) <= 20:
                message = ""
                emojis = {}
                emojis[0] = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
                emojis[1] = [
                    '🟤', '🔴', '🟠', '🟡', '🟢', '🔵', '🟣', '🔘', '❤', '💜',
                    '🟫', '🟥', '🟧', '🟨', '🟩', '🟦', '🟪', '🔳', '🧡', '💙'
                ]
                mixable = True
                if len(propositions) <= 10:
                    emojis_chosen = emojis[randint(0, len(emojis) - 1)]
                    emojis_chosen = emojis_chosen[:10]
                    if len(propositions) <= 8:
                        emojis_chosen = emojis_chosen[:8]
                else:
                    emojis_chosen = emojis[randint(1, len(emojis) - 1)]
                if emojis[0][0] in emojis_chosen: # rajouter ici les listes qui ne doivent pas être mélanger
                    mixable = False
                if mixable:
                    shuffle(emojis_chosen)
                for i in range(len(args[1:])):
                    message += f"{emojis_chosen[i]} -> {propositions[i]}\n"
                embed = discord.Embed(title = question, description = message,color = randint(0, 0xFFFFFF)).set_footer(text = self.user_or_nick(ctx.author), icon_url = ctx.author.avatar_url)
                sondage = await ctx.send(embed = embed)
                for i in range(len(args[1:])):
                    await sondage.add_reaction(emoji = emojis_chosen[i])
                return await ctx.message.add_reaction(emoji = '✅')
            else:
                return await ctx.send(f"Désolé, mais tu as mis trop de possibilités (maximum : 20)")
        else:
            return await ctx.send(f'Désolé, mais il manque des arguments : `.sondage "<Question>" "<Proposition1>" "<Proposition...>" "<Proposition20>"`')
    def user_or_nick(self, user):
        if user.nick:
            return f"{user.nick} ({user.name}#{user.discriminator})"
        else:
            return f"{user.name}#{user.discriminator}"
import discord, pytz, time, os
from discord.ext import commands
from random import randint, shuffle
from datetime import datetime
from pytz import timezone
import re, asyncio

def setup(client):
    client.add_cog(Utils(client))

class Utils(commands.Cog):
    """Commandes essentielles."""

    def __init__(self, client):
        self.client = client
        self.customTimezone = os.environ['TIMEZONE']


    @commands.command(name='ping')
    async def _ping(self, ctx, *, question = '0'):
        """Affiche mon ping.⁢⁢⁢⁢⁢\n	➡ Syntaxe: .ping [help]⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        if question == 'help':
            return await ctx.send(embed = discord.Embed(color = discord.Colour.random(), description = ":hourglass: correspond au temps entre deux battements de cœurs\n\n:stopwatch: correspond au temps que met le client a calculer le ping\n\n:heartbeat: correspond au temps que met le client a réagir au messages"))
        else:
            now = int(round(time.time() * 1000))
            ping = now - int(round(ctx.message.created_at.timestamp() * 1000))
            embed = discord.Embed(description = 'Pinging...')
            message = await ctx.send(embed = embed)
            ping2 = int(round(time.time() * 1000)) - now
            await message.edit(embed = discord.Embed(color = discord.Colour.random(), description = f':hourglass: {round(self.client.latency * 1000)} ms\n\n:stopwatch: {ping2} ms\n\n:heartbeat: {ping} ms'))
            await ctx.message.add_reaction(emoji = '✅')

    @commands.command(name='avatar')
    async def _avatar(self, ctx, *, user = '0'):
        """Affiche ton avatar ou celui que tu mentionnes.\n	➡ Syntaxe: .avatar [user]"""
        if user == '0':
            user = ctx.author
        else:
            user = self.client.get_user(int(user[2:-1].replace("!","")))
        await ctx.message.add_reaction(emoji = '✅')
        embed = discord.Embed(description = f"[lien vers la photo de profil]({user.avatar_url}) de {user.mention}", color = discord.Colour.random())
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
        embed = discord.Embed(color = discord.Colour.random(), title = 'Calculatrice')
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
            embed = discord.Embed(description = text, color = discord.Colour.random())
            embed.set_author(name = f"Mémo noté depuis {ctx.guild.name}", icon_url = ctx.author.avatar_url)
            embed.set_footer(text = f'📝 le {datetime.now(pytz.timezone(self.customTimezone)).strftime("%d/%m/%Y à %H:%M:%S")}')
            await ctx.author.send(embed = embed)
            return await ctx.send("Tu viens de recevoir ton mémo !", delete_after = 5)
    @_memo.error
    async def _note_error(self, ctx, error):
        if str(error) == "text is a required argument that is missing.":
            await ctx.send(f"Vous devez renseigner un message : `{ctx.prefix}note/memo <message>⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢`.")

    @commands.command(name='infos', aliases = ['info'])
    async def _infos(self, ctx):
        """Donne des infos sur le bot.\n	➡ Syntaxe: .infos/info⁢"""
        appinfo = await self.client.application_info()

        embed = discord.Embed(color = discord.Colour.random())

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
        nombreServeur = len(self.client.guilds)
        
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "README.md"), "r") as file:
            for versionNumber in re.findall(r'https://img.shields.io/badge/version-(\d+\.\d+)', file.readlines()[2]):
                version = versionNumber

        embed.add_field(name = "Dev", value = f"[{appinfo.owner}](https://github.com/Mylloon)")
        embed.add_field(name = f"Serveur{'s' if nombreServeur > 1 else ''}", value = f"`{nombreServeur}`")
        embed.add_field(name = f"Membre{'s' if total_unique > 1 else ''}", value = f"`{total_unique}` au total\n`{total_online}` en ligne")
        embed.add_field(name = f"Salon{'s' if (text + voice) > 1 else ''}", value = f"`{text}` textuel{'s' if text > 1 else ''}\n`{voice}` voca{'ux' if voice > 1 else 'l'}")
        embed.add_field(name = "Prefix", value = f"`{ctx.prefix}`")
        embed.add_field(name = "Code source", value = f"[Lien Github](https://github.com/Confrerie-du-Kassoulait/KassouBot/)")
        embed.add_field(name = "Timezone", value = f"`{self.customTimezone}`")
        embed.add_field(name = "Version", value = f"`{version}`")
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
            embed = discord.Embed(title = f"Map Mira HQ d'Among Us", color = discord.Colour.random(), description = f"[lien de l'image]({image})")
            embed.set_image(url = image)
            await ctx.send(embed = embed)
            await ctx.message.add_reaction(emoji = '✅')
        elif map.lower() in self._map_list_among_us("polus"):
            image = "https://i.imgur.com/mhFmcw3.jpg"
            embed = discord.Embed(title = f"Map Polus d'Among Us", color = discord.Colour.random(), description = f"[lien de l'image]({image})")
            embed.set_image(url = image)
            await ctx.send(embed = embed)
            await ctx.message.add_reaction(emoji = '✅')
        elif map.lower() in self._map_list_among_us("skeld"):
            image = "https://i.imgur.com/OSXI4Zv.jpg"
            embed = discord.Embed(title = f"Map The Skeld d'Among Us", color = discord.Colour.random(), description = f"[lien de l'image]({image})")
            embed.set_image(url = image)
            await ctx.send(embed = embed)
            await ctx.message.add_reaction(emoji = '✅')
        elif map.lower() in self._map_list_among_us("airship"):
            image = "https://i.imgur.com/cm8Wogw.png"
            embed = discord.Embed(title = f"Map Airship d'Among Us", color = discord.Colour.random(), description = f"[lien de l'image]({image})")
            embed.set_image(url = image)
            await ctx.send(embed = embed)
            await ctx.message.add_reaction(emoji = '✅')
        else:
            await ctx.send(f"`{ctx.prefix}amongus <mira/polus/skeld/airship>`")

    @commands.command(name='whois')
    async def _whois(self, ctx, *user: discord.Member):
        """Affiche les infos sur l'utilisateur.⁢⁢⁢⁢⁢\n	➡ Syntaxe: .whois [user]⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        if len(user) <= 1:
            if user == ():
                user = [ctx.author]
            nom = f"{user[0].name}#{user[0].discriminator}"
            if user[0].nick:
                nom = f"{user[0].nick} ({user[0].name}#{user[0].discriminator})"
            embed = discord.Embed(color = discord.Colour.random()).set_author(name = nom, icon_url = user[0].avatar_url)
            
            embed.add_field(name = "ID", value = user[0].id)
            
            value = str(user[0].created_at.astimezone(timezone(self.customTimezone)))[:-13].replace('-', '/').split()
            embed.add_field(name = "Compte créé le", value = f"{value[0][8:]}/{value[0][5:-3]}/{value[0][:4]} à {value[1]}")
            
            embed.add_field(name = "Âge du compte", value = self._ageLayout(self._get_age(user[0].created_at)))
            
            embed.add_field(name = "Mention", value = user[0].mention)
            
            value = str(user[0].joined_at.astimezone(timezone(self.customTimezone)))[:-13].replace('-', '/').split()
            embed.add_field(name = "Serveur rejoint le", value = f"{value[0][8:]}/{value[0][5:-3]}/{value[0][:4]} à {value[1]}")
            
            embed.add_field(name = "Est sur le serveur depuis", value = self._ageLayout(self._get_age(user[0].joined_at)))
            await ctx.message.add_reaction(emoji = '✅')
            return await ctx.send(embed = embed)
        return await ctx.send(f"Tu mentionnes trop d'utilisateurs :  `{ctx.prefix}whois [@Membre]`")

    def _get_age(self, date):
        joursRestants = datetime.now() - date
        years = joursRestants.total_seconds() / (365.242 * 24 * 3600)
        months = (years - int(years)) * 12
        days = (months - int(months)) * (365.242 / 12)
        hours = (days - int(days)) * 24
        minutes = (hours - int(hours)) * 60
        seconds = (minutes - int(minutes)) * 60
        return (int(years), int(months), int(days),  int(hours), int(minutes), int(seconds))

    def _ageLayout(self, tuple):
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

    def _userOrNick(self, user):
        if user == None:
            return "Utilisateur inconnu" # Mauvais copié/collé -> changement d'ID
        if user.nick:
            return f"{user.nick} ({user.name}#{user.discriminator})"
        else:
            return f"{user.name}#{user.discriminator}"

    def _cleanUser(self, ctx, stringMessage, stringID):
        stringMessage = stringMessage.replace("<@!", "").replace(">", "").replace("<@", "")
        associatedID = self._userOrNick(ctx.author.guild.get_member(int(stringID)))
        try:
            stringMessage = stringMessage.replace(stringID, associatedID)
        except:
            pass
        return stringMessage

    def _cleanCodeStringWithMention(self, string):
        string = f"`{self._removeStartEndSpacesString(string)}`"
        findedMention = self._getMentionInString(string)
        for i in range(0, len(findedMention)):
            string = string.replace(findedMention[i], f"`{findedMention[i]}`") # conserve la mention dans le message
        if string.startswith("``<@"): # conserve le format quand mention au début de la string
            string = string[2:]
        if string.endswith(">``"): # conserve le format quand mention à la fin de la string
            string = string[:-2]
        return string

    def _getMentionInString(self, string):
        findedMention = []
        for findingMention in re.findall(r'<@[!]?\d*>', string): # récupération mention dans la string
            findedMention.append(findingMention)
        findedMention = list(dict.fromkeys(findedMention)) # suppression doublon de mention
        return findedMention
    
    def _removeStartEndSpacesString(self, string):
        while string.startswith(" "):
            string = string[1:]
        while string.endswith(" "):
            string = string[:-1]
        return string

    @commands.command(name='sondage')
    async def _sondage(self, ctx, *args):
        """Fais un sondage.⁢⁢⁢⁢⁢\n	➡ Syntaxe: .sondage "<Question>" "<Proposition1>" "<Proposition...>" "<Proposition20>" """
        args = list(args)
        if len(args) > 2:
            question = args[0]
            for i in re.findall(r'\d+', question):
                question = self._cleanUser(ctx, question, i)
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
                embed = discord.Embed(title = question, description = message, color = discord.Colour.random()).set_footer(text = self._userOrNick(ctx.author), icon_url = ctx.author.avatar_url)
                sondage = await ctx.send(embed = embed)
                for i in range(len(args[1:])):
                    await sondage.add_reaction(emoji = emojis_chosen[i])
                return await ctx.message.add_reaction(emoji = '✅')
            else:
                return await ctx.send(f"Désolé, mais tu as mis trop de possibilités (maximum : 20)")
        else:
            return await ctx.send(f'Désolé, mais il manque des arguments : `{ctx.prefix}sondage "<Question>" "<Proposition1>" "<Proposition...>" "<Proposition20>"`')

    @commands.command(name='avis', aliases=['vote'])
    async def _avis(self, ctx, *args):
        """Demande un avis.⁢⁢⁢⁢⁢\n	➡ Syntaxe: .avis/vote "[Titre]" "<Demande>" """
        args = list(args)
        if len(args) > 2 or len(args) == 0:
            return await ctx.send("Désolé, la syntaxe est mauvaise.")
        else:
            if len(args) == 1: # si aucun titre défini
                titre = "Nouveau vote"
            else: # si titre défini
                titre = args[0]
                for findedId in re.findall(r'\d+', titre): # récupération mention dans titre
                    titre = self._cleanUser(ctx, titre, findedId)
                args = args[1:]
            embed = discord.Embed(title = titre, description = self._cleanCodeStringWithMention(args[0]), color = discord.Colour.random()).set_footer(text = self._userOrNick(ctx.author), icon_url = ctx.author.avatar_url)
            message = await ctx.send(embed = embed)
            reactions = ['✅', '🤷', '❌']
            for i in reactions:
                await message.add_reaction(emoji = i)
            return await ctx.message.delete()

    @commands.command(name='reminder', aliases=["remind", "remindme"])
    async def _reminder(self, ctx, time, *, reminder):
        """Met en place un rappel.⁢⁢⁢⁢⁢\n	➡ Syntaxe: .reminder/remind/remindme <temps (d/h/m/s)>[@] <message> """
        embed = discord.Embed(color = 0xC41B1B)
        seconds = 0
        timestamp = datetime.utcnow()
        mention = False
        if reminder:
            if time.lower().endswith("@"):
                time = time[:-1]
                mention = True
            try:
                if time.lower().endswith("d"):
                    seconds += int(time[:-1]) * 60 * 60 * 24
                    _seconds = seconds // 60 // 60 // 24
                    counter = f"{_seconds} jour{'s' if _seconds > 1 else ''}"
                if time.lower().endswith("h"):
                    seconds += int(time[:-1]) * 60 * 60
                    _seconds = seconds // 60 // 60
                    counter = f"{_seconds} heure{'s' if _seconds > 1 else ''}"
                elif time.lower().endswith("m"):
                    seconds += int(time[:-1]) * 60
                    _seconds = seconds // 60
                    counter = f"{_seconds} minute{'s' if _seconds > 1 else ''}"
                elif time.lower().endswith("s"):
                    seconds += int(time[:-1])
                    counter = f"{seconds} seconde{'s' if seconds > 1 else ''}"
            except:
                pass
            if seconds == 0:
                embed.add_field(name="Attention", value="Mauvais format pour le temps, `d` pour jour, `h` pour heure, `m` pour minute, `s` pour seconde (ne fonctionne qu'avec une seule unité)\nMet un `@` accolée à l'unité pour mentionner les gens mentionner dans ton message.")
            elif seconds > 7776000: # 90 * 60 * 60 * 24
                embed.add_field(name="Attention", value="Tu as spécifié une durée trop longue, la durée maximum étant de 90 jours.")
            else:
                await ctx.send(f"Ok, je t'en parles dans {counter} !")
                await asyncio.sleep(seconds)
                message = ctx.author.mention
                if mention:
                    mentionList = self._getMentionInString(reminder)
                    for i in mentionList:
                        message += f" {i}"
                try:
                    await ctx.message.add_reaction(emoji = '✅')
                except:
                    pass
                return await ctx.send(message, embed = discord.Embed(description = self._cleanCodeStringWithMention(reminder), timestamp = timestamp, color = discord.Colour.random()).set_footer(text=f"Message d'il y a {counter}"))
        else:
            embed.add_field(name="Attention", value="Mauvaise syntaxe : reminder <temps> <message>")
        await ctx.send(embed = embed)

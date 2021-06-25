import discord
from os import environ, path
from re import findall
from discord.ext import commands, tasks
from random import randint, shuffle
from discord_slash import cog_ext
from utils.reminder import Reminder
from utils.core import map_list_among_us, getURLsInString, getMentionInString, cleanCodeStringWithMentionAndURLs, cleanUser, userOrNick
from utils.core import mySendHidden, mentionToUser, getChangelogs, isSlash
from utils.time import stringTempsVersSecondes, nowUTC, intToDatetime, timedeltaToString, timestampScreen, getAge, ageLayout, nowCustom

def setup(client):
    client.add_cog(Utils(client))

class Utils(commands.Cog):
    """Commandes essentielles."""
    def __init__(self, client):
        self.client = client
        self.customTimezone = environ['TIMEZONE']
        self._reminderLoop.start()

    @commands.command(name='ping')
    async def _ping(self, ctx, *arg):
        arg, fromSlash, _ = isSlash(arg)

        if arg == 'help':
            return await mySendHidden(ctx, fromSlash, embed = discord.Embed(color = discord.Colour.random(), description =
                ":hourglass: correspond au temps entre deux battements de cœurs\n\n \
                :heartbeat: correspond au temps que met le client a réagir au messages (0 est normal lors de l'utilisation d'une commande slash)\n\n \
                :stopwatch: correspond au temps que met le client a calculer le ping"
            ))
        else:
            now = int(round(nowCustom() * 1000))
            if fromSlash != True:
                ping = now - int(round(ctx.message.created_at.timestamp() * 1000))
            else:
                ping = now - int(round(ctx.slash_created_at * 1000))
            embed = discord.Embed(description = 'Pinging...')
            message = await ctx.send(embed = embed)
            ping2 = int(round(nowCustom() * 1000)) - now
            await message.edit(embed = discord.Embed(color = discord.Colour.random(), description = f':hourglass: {round(self.client.latency * 1000)} ms\n\n:heartbeat: {ping} ms\n\n:stopwatch: {ping2} ms'))
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '✅')
    @cog_ext.cog_slash(name="ping", description = "Affiche mon ping, mettre 'help' en argument pour connaître à quoi correspond les données.")
    async def __ping(self, ctx, arg = None):
        ctx.slash_created_at = nowCustom()
        if arg == None:
            return await self._ping(ctx, True)
        else:
            return await self._ping(ctx, arg, True)

    @commands.command(name='avatar')
    async def _avatar(self, ctx, *user):
        """Affiche ton avatar ou celui que tu mentionnes.\n	➡ Syntaxe: {PREFIX}avatar [user]"""
        user, fromSlash, _ = isSlash(user)

        if user == None:
            user = ctx.author
        else:
            user = self.client.get_user(mentionToUser(user))
        if fromSlash != True:
            await ctx.message.add_reaction(emoji = '✅')
        embed = discord.Embed(description = f"[lien vers la photo de profil]({user.avatar_url}) de {user.mention}", color = discord.Colour.random())
        embed.set_author(name = f"Photo de profil de {user.name}")
        embed.set_image(url = user.avatar_url)
        await ctx.send(embed = embed)
    @cog_ext.cog_slash(name="avatar", description = "Affiche ton avatar ou celui que tu mentionnes.")
    async def __avatar(self, ctx, user = None):
        if user == None:
            return await self._avatar(ctx, True)
        else:
            return await self._avatar(ctx, user, True)

    @commands.command(name='calc')
    async def _calc(self, ctx, *calcul):
        """Calculatrice.\n	➡ Syntaxe: {PREFIX}calc <calcul>⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        calcul, fromSlash, _ = isSlash(calcul)
        if calcul == None:
            raise ModuleNotFoundError

        equation = calcul.replace('^', '**').replace('x', '*').replace('×', '*').replace('÷', '/').replace('≥', '>=').replace('≤', '<=')
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
                return await mySendHidden(ctx, fromSlash, "Tu ne peux pas diviser par 0.")
        except TypeError:
            return await mySendHidden(ctx, fromSlash, "Requête de calcul invalide.")
        if '.' in answer:
            aftercomma = answer.split(".")[1]
            if len(aftercomma) > 2:
                answer = str(round(float(answer),2))
                equation = f"'{equation}' arrondi à 2"
        equation = equation.replace('*', '×').replace('/', '÷').replace('>=', '≥').replace('<=', '≤')
        embed = discord.Embed(color = discord.Colour.random(), title = 'Calculatrice')
        embed.set_footer(text = userOrNick(ctx.author), icon_url = ctx.author.avatar_url)

        embed.add_field(name = 'Calcul :', value = equation, inline = False)
        embed.add_field(name = 'Réponse :', value = answer.replace('False', 'Faux').replace('True', 'Vrai'), inline = False)
        if fromSlash != True:
            await ctx.message.add_reaction(emoji = '✅')
        await ctx.send(embed = embed)
    @_calc.error
    async def _calc_error(self, ctx, _):
        await ctx.send("Tu n'as pas spécifié de calcul.")
    @cog_ext.cog_slash(name="calc", description = "Calculatrice.")
    async def __calc(self, ctx, calcul):
        return await self._calc(ctx, calcul, True)

    @commands.command(name='syntax')
    async def _syntax(self, ctx, fromSlash = None):
        """Informations pour bien éditer son texte.⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        if fromSlash != True:
            fromSlash = False
        separateur = "-----------------------------------------------------\n"
        syntaxe = separateur
        syntaxe += discord.utils.escape_markdown("```js\n")
        syntaxe += discord.utils.escape_markdown("//code en js (possible de remplacer 'js' par d'autres languages . adaptez le !)\n")
        syntaxe += discord.utils.escape_markdown('console.log("hi");\n')
        syntaxe += discord.utils.escape_markdown("```\n")
        syntaxe += "```js\n"
        syntaxe += "//code en js (possible de remplacer 'js' par d'autres languages . adaptez le !)\n"
        syntaxe += 'console.log("hi");\n'
        syntaxe += "```\n"
        syntaxe += "Si ton code est trop long, mets le sur <https://pastebin.com/>\n"
        syntaxe += separateur
        syntaxe += discord.utils.escape_markdown("`code sur une seule ligne`\n")
        syntaxe += "`code sur une seule ligne`\n"
        syntaxe += separateur
        syntaxe += discord.utils.escape_markdown("*texte en italique*\n")
        syntaxe += "*texte en italique*\n"
        syntaxe += separateur
        syntaxe += discord.utils.escape_markdown("**text en gras**\n")
        syntaxe += "**text en gras**\n"
        syntaxe += separateur
        syntaxe += discord.utils.escape_markdown("<<https://www.youtube.com/watch?v=GhuYKL5NUYg>>\n")
        syntaxe += "Un lien entre crochet, ça empêche Discord de rajouté son intégration automatique (mais le lien fonctionnera toujours).\n"
        syntaxe += separateur
        syntaxe += discord.utils.escape_markdown("__texte souligné__\n")
        syntaxe += "__texte souligné__\n"
        syntaxe += separateur
        syntaxe += discord.utils.escape_markdown("~~texte barré~~\n")
        syntaxe += "~~texte barré~~\n"
        syntaxe += separateur
        syntaxe += discord.utils.escape_markdown("~~__***text en italique-gras-souligné-barré***__~~\n")
        syntaxe += "~~__***text en italique-gras-souligné-barré***__~~\n"
        syntaxe += separateur
        syntaxe += discord.utils.escape_markdown("\:joy: <- l'emoji ne va pas fonctionné grâce au \ \n")
        syntaxe += "\:joy: <- l'emoji ne va pas fonctionné grâce au \ \n"
        syntaxe += separateur
        syntaxe += discord.utils.escape_markdown("> cette ligne est cité\npas celle là\n")
        syntaxe += "> cette ligne est cité\npas celle là\n"
        syntaxe += separateur
        syntaxe += discord.utils.escape_markdown(">>> cette ligne est cité\ncelle là aussi (et elles le seront toutes!)\n")
        syntaxe += ">>> cette ligne est cité\ncelle là aussi (et elles le seront toutes!)\n"
        try:
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '✅')
        except:
            pass
        await mySendHidden(ctx, fromSlash, syntaxe)
    @cog_ext.cog_slash(name="syntax", description = "Informations pour bien éditer son texte.")
    async def __syntax(self, ctx):
        return await self._syntax(ctx, True)

    @commands.command(name='memo', aliases = ['note'])
    async def _memo(self, ctx, *text):
        """T'envoie un petit memo par message privé.\n	➡ Syntaxe: {PREFIX}memo/note <message>⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        _, fromSlash, text = isSlash(text)
        if len(text) > 0:
            text = " ".join(text)
        else:
            raise ModuleNotFoundError

        if len(text) <= 5:
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '❌')
            return await mySendHidden(ctx, fromSlash, "Ta note doit au moins faire 5 caractères.")
        elif len(text) >= 2048:
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '❌')
            return await ctx.send(ctx, fromSlash, "Ta note doit faire moins de 2048 caractères.")
        else:
            if fromSlash != True:
                await ctx.message.delete()
            embed = discord.Embed(description = text, color = discord.Colour.random())
            embed.set_author(name = f"Mémo noté depuis {ctx.guild.name}", icon_url = ctx.author.avatar_url)
            embed.set_footer(text = f'📝 le {timestampScreen(intToDatetime(nowUTC()))}')
            await ctx.author.send(embed = embed)
            
            return await mySendHidden(ctx, fromSlash, "Tu viens de recevoir ton mémo !", delete_after = 5)
    @_memo.error
    async def _memo_error(self, ctx, error):
        if str(error) == "text is a required argument that is missing.":
            await ctx.send(f"Vous devez renseigner un message : `{ctx.prefix}memo/note <message>⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢`.")
    @cog_ext.cog_slash(name="note", description = "T'envoie un petit memo par message privé.")
    async def __memo(self, ctx, memo):
        return await self._memo(ctx, memo, True)

    @commands.command(name='infos', aliases = ['info'])
    async def _infos(self, ctx, fromSlash = None):
        """Donne des infos sur le bot.\n	➡ Syntaxe: {PREFIX}infos/info⁢"""
        if fromSlash != True:
            fromSlash = False
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
        
        with open(path.join(path.dirname(path.dirname(path.dirname(__file__))), "README.md"), "r") as file:
            version = findall(r'https://img.shields.io/badge/version-(\d+\.\d+)', file.readlines()[2])[0]

        embed.add_field(name = "Dev", value = f"[{appinfo.owner}](https://github.com/Mylloon)")
        embed.add_field(name = f"Serveur{'s' if nombreServeur > 1 else ''}", value = f"`{nombreServeur}`")
        embed.add_field(name = f"Membre{'s' if total_unique > 1 else ''}", value = f"`{total_unique}` au total\n`{total_online}` en ligne")
        embed.add_field(name = f"Salon{'s' if (text + voice) > 1 else ''}", value = f"`{text}` textuel{'s' if text > 1 else ''}\n`{voice}` voca{'ux' if voice > 1 else 'l'}")
        embed.add_field(name = "Prefix", value = f"`{ctx.prefix}`")
        embed.add_field(name = "Code source", value = "[Lien Github](https://github.com/Confrerie-du-Kassoulait/KassouBot/)")
        embed.add_field(name = "Timezone", value = f"`{self.customTimezone}`")
        embed.add_field(name = "Version", value = f"`{version}`")
        changes = getChangelogs(version)
        if changes != None and changes != 0:
            embed.add_field(name = "Changements", value = f"[Lien Github]({changes[0]})")
        embed.set_footer(text = f"Basé sur discord.py {discord.__version__}")
        try:
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '✅')
        except:
            pass
        await ctx.send(embed = embed)
    @cog_ext.cog_slash(name="infos", description = "Donne des infos sur le bot.")
    async def __infos(self, ctx):
        ctx.prefix = "/"
        return await self._infos(ctx, True)

    @commands.command(name='amongus')
    async def _amongus(self, ctx, *map):
        """Affiche la carte voulue d'Among Us.⁢⁢⁢⁢⁢\n	➡ Syntaxe: {PREFIX}amongus <mira/polus/skeld/airship>⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        _, fromSlash, map = isSlash(map)
        if len(map) > 0:
            map = " ".join(map)
        else:
            map = "0"

        if map.lower() in map_list_among_us("mira"):
            image = "https://i.imgur.com/6ijrH1h.jpg"
            embed = discord.Embed(title = f"Map Mira HQ d'Among Us", color = discord.Colour.random(), description = f"[lien de l'image]({image})")
            embed.set_image(url = image)
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '✅')
            await ctx.send(embed = embed)
        elif map.lower() in map_list_among_us("polus"):
            image = "https://i.imgur.com/mhFmcw3.jpg"
            embed = discord.Embed(title = f"Map Polus d'Among Us", color = discord.Colour.random(), description = f"[lien de l'image]({image})")
            embed.set_image(url = image)
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '✅')
            await ctx.send(embed = embed)
        elif map.lower() in map_list_among_us("skeld"):
            image = "https://i.imgur.com/OSXI4Zv.jpg"
            embed = discord.Embed(title = f"Map The Skeld d'Among Us", color = discord.Colour.random(), description = f"[lien de l'image]({image})")
            embed.set_image(url = image)
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '✅')
            await ctx.send(embed = embed)
        elif map.lower() in map_list_among_us("airship"):
            image = "https://i.imgur.com/cm8Wogw.png"
            embed = discord.Embed(title = f"Map Airship d'Among Us", color = discord.Colour.random(), description = f"[lien de l'image]({image})")
            embed.set_image(url = image)
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '✅')
            await ctx.send(embed = embed)
        else:
            await mySendHidden(ctx, fromSlash, f"`{ctx.prefix}amongus <mira/polus/skeld/airship>`")
    @commands.command(name='among', hidden = True)
    async def _among(self, ctx, *, args = ""):
        """Raccourci à la commande amongus⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        if not args == "":
            args = args.split()
            del args[0]
            args = " ".join(args)
            if args.lower() in map_list_among_us("all"):
                await ctx.invoke(self.client.get_command("amongus"), map=args)
            else:
                await ctx.invoke(self.client.get_command("amongus"))
        else:
            await ctx.message.add_reaction(emoji = '❓')
    @cog_ext.cog_slash(name="amongus", description = "Affiche la carte voulue d'Among Us. Carte dispo : <mira/polus/skeld/airship>")
    async def __amongus(self, ctx, map):
        ctx.prefix = "/"
        return await self._amongus(ctx, map, True)

    @commands.command(name='whois')
    async def _whois(self, ctx, *user: discord.Member):
        """Affiche les infos sur l'utilisateur.⁢⁢⁢⁢⁢\n	➡ Syntaxe: {PREFIX}whois [user]⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        _, fromSlash, user = isSlash(user)

        if len(user) <= 1:
            if user == ():
                user = [ctx.author]
            nom = f"{user[0].name}#{user[0].discriminator}"
            if user[0].nick:
                nom = f"{user[0].nick} ({user[0].name}#{user[0].discriminator})"
            embed = discord.Embed(color = discord.Colour.random()).set_author(name = nom, icon_url = user[0].avatar_url)
            
            embed.add_field(name = "ID", value = user[0].id)
            
            embed.add_field(name = "Compte créé le", value = timestampScreen(user[0].created_at))
            
            embed.add_field(name = "Âge du compte", value = ageLayout(getAge(user[0].created_at)))
            
            embed.add_field(name = "Mention", value = user[0].mention)
            
            embed.add_field(name = "Serveur rejoint le", value = timestampScreen(user[0].joined_at))
            
            embed.add_field(name = "Est sur le serveur depuis", value = ageLayout(getAge(user[0].joined_at)))
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '✅')
            return await ctx.send(embed = embed)
        return await ctx.send(f"Tu mentionnes trop d'utilisateurs : `{ctx.prefix}whois [@membre]`")
    @cog_ext.cog_slash(name="whois", description = "Affiche les infos sur l'utilisateur.")
    async def __whois(self, ctx, user: discord.Member = None):
        ctx.prefix = "/" # pas sûr que ce soit utile
        if user == None:
            return await self._whois(ctx, True)
        else:
            return await self._whois(ctx, user, True)

    @commands.command(name='sondage')
    async def _sondage(self, ctx, *args):
        """Fais un sondage.⁢⁢⁢⁢⁢\n	➡ Syntaxe: {PREFIX}sondage "<Question>" "<Proposition1>" "<Proposition...>" "<Proposition20>" """
        _, fromSlash, args = isSlash(args)
        if type(args[0]) == list:
            args = args[0]

        args = list(args)
        if len(args) > 2:
            question = args[0]
            for i in findall(r'\d+', question):
                question = cleanUser(ctx, question, i)
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
                embed = discord.Embed(title = question, description = message, color = discord.Colour.random()).set_footer(text = f"Sondage de {userOrNick(ctx.author)}", icon_url = ctx.author.avatar_url)
                sondage = await ctx.send(embed = embed)
                for i in range(len(args[1:])):
                    await sondage.add_reaction(emoji = emojis_chosen[i])
                if fromSlash != True:
                    return await ctx.message.add_reaction(emoji = '✅')
            else:
                return await ctx.send(f"Désolé, mais tu as mis trop de possibilités (maximum : 20)")
        else:
            return await ctx.send(f'Désolé, mais il manque des arguments : `{ctx.prefix}sondage "<Question>" "<Proposition1>" "<Proposition...>" "<Proposition20>"`')    
    @cog_ext.cog_slash(name="sondage", description = "Fais un sondage.")
    async def __sondage(self, ctx, question, prop1, prop2, prop3 = None, prop4 = None,
    prop5 = None, prop6 = None, prop7 = None, prop8 = None, prop9 = None, prop10 = None,
    prop11 = None, prop12 = None, prop13 = None, prop14 = None, prop15 = None, prop16 = None,
    prop17 = None, prop18 = None, prop19 = None, prop20 = None):
        ctx.prefix = "/"
        args = [question, prop1, prop2, prop3, prop4, prop5, prop6, prop7, prop8,
        prop9, prop10, prop11, prop12, prop13, prop14, prop15, prop16,
        prop17, prop18, prop19, prop20]
        for i in range(3, 20): # suppression des None
            if args[i] == None:
                args = args[:i]
                break
        return await self._sondage(ctx, args, True)

    @commands.command(name='avis', aliases=['vote'])
    async def _avis(self, ctx, *args):
        """Demande un avis.⁢⁢⁢⁢⁢\n	➡ Syntaxe: {PREFIX}avis/vote "[Titre]" "<Demande>" """
        _, fromSlash, args = isSlash(args)
        if type(args[0]) == list:
            args = args[0]

        args = list(args)
        if len(args) > 2 or len(args) == 0:
            return await ctx.send("Désolé, la syntaxe est mauvaise.")
        else:
            if len(args) == 1: # si aucun titre défini
                titre = "Nouveau vote"
            else: # si titre défini
                titre = args[0]
                for findedId in findall(r'\d+', titre): # récupération mention dans titre
                    titre = cleanUser(ctx, titre, findedId)
                args = args[1:]
            embed = discord.Embed(title = titre, description = cleanCodeStringWithMentionAndURLs(args[0]), color = discord.Colour.random()).set_footer(text = f"Sondage de {userOrNick(ctx.author)}", icon_url = ctx.author.avatar_url)
            message = await ctx.send(embed = embed)
            reactions = ['✅', '🤷', '❌']
            for i in reactions:
                await message.add_reaction(emoji = i)
            if fromSlash != True:
                return await ctx.message.delete()
    @cog_ext.cog_slash(name="avis", description = "Demande un avis, si 2 arguments, alors l'argument 1 est le titre, sinon c'est la demande.")
    async def __avis(self, ctx, titreoudemande, demande = None):
        args = [titreoudemande, demande]
        if args[1] == None:
            args = args[:1]
        return await self._avis(ctx, args, True)

    @commands.command(name='reminder', aliases=["remind", "remindme", "rappel"])
    async def _reminder(self, ctx, time, *reminder):
        """Met en place un rappel.⁢⁢⁢⁢⁢\n	➡ Syntaxe: {PREFIX}reminder/remind/remindme/rappel <temps>[@] [message]"""
        _, fromSlash, reminder = isSlash(reminder)
        if len(reminder) > 0:
            reminder = " ".join(reminder)
        else:
            reminder = None

        embed = discord.Embed(color = 0xC41B1B)
        extrarg = 0
        guildID = ctx.guild.id # can be set to 0 if its a DM message, so it can be see from anywhere
        destination = "ici"
        if not reminder:
            reminder = "Notification"
        if time == "help":
            seconds = 0
        else:
            if time.endswith("@"):
                time = time[:-1]
                extrarg = 1
            if time.lower().endswith("p"):
                time = time[:-1]
                extrarg = 2
                guildID = 0
                destination = "en MP"
            seconds = stringTempsVersSecondes(time)
            if type(seconds) != int:
                if fromSlash != True:
                    await ctx.message.add_reaction(emoji = '❓')
                return await mySendHidden(ctx, fromSlash, seconds)
        if seconds == 0:
            embed.add_field(name="Attention", value=
                "Format pour le temps : `d` ou `j` pour jour, `h` pour heure, `m` pour minute, `s` pour seconde (légères variances acceptés aussi). \
                \nMet un `@` accolée aux temps pour mentionner les gens mentionner dans ton message. \
                \nMet un `P` accolée au temps pour que le bot te DM au lieu de t'envoyer un message dans ce salon."
            )
        elif seconds > (50 * (86400 * 365.242)): # 50 ans
            embed.add_field(name="Attention", value="Tu as spécifié une durée trop longue, la durée maximum étant de 50 ans.")
        else:
            now = int(nowUTC())
            messageID = None
            if fromSlash != True:
                messageID = ctx.message.id
            Reminder().ajoutReminder(messageID, ctx.channel.id, extrarg, reminder, now, now + seconds, ctx.author.id, guildID)
            return await mySendHidden(ctx, fromSlash, f"Ok, je t'en parles {destination} dans {timedeltaToString(seconds)} avec 1m de retard maximum.")
        await mySendHidden(ctx, fromSlash, embed = embed)
    @_reminder.error
    async def _reminder_error(self, ctx, error):
        if 'time is a required argument that is missing.' in str(error):
            await ctx.send("Tu n'as pas spécifié de durée.")
    @cog_ext.cog_slash(name="reminder", description = "Met en place un rappel.")
    async def __reminder(self, ctx, time, reminder = None):
        if reminder == None:
            return await self._reminder(ctx, time, True)
        else:
            return await self._reminder(ctx, time, reminder, True)

    @tasks.loop(minutes = 1)
    async def _reminderLoop(self):
        """Méthode qui se répète toute les minutes pour vérifier si des rappels n'ont pas expirés, si expirés, les envoient."""
        expiration = Reminder().recuperationExpiration(int(nowUTC())) # on récupères les éléments expirés
        for expired in expiration: # on regarde tout les éléments expirés
            reminder = expired[2] # message
            userID = expired[4] # personne qui a fait le rappel
            channel = self.client.get_channel(expired[0]) # salon du message
            finalEmbed = discord.Embed(description = cleanCodeStringWithMentionAndURLs(reminder), timestamp = intToDatetime(expired[3]), color = discord.Colour.random())
            if expired[1] == 2: # s'il faut envoyer en DM le message
                user =  self.client.get_user(userID)
                if user == None: # si l'utilisateur n'est pas trouvé
                    return Reminder().suppressionReminder(expired[5]) # suppression du rappel
                channel = await user.create_dm() # envoie en DM
                userID = None # plus de mention
                sourceMessage = None # plus de message source
            elif channel == None: # si le salon n'existe plus
                user =  self.client.get_user(userID)
                if user == None: # si l'utilisateur n'est pas trouvé
                    return Reminder().suppressionReminder(expired[5]) # suppression du rappel
                channel = await user.create_dm() # envoie en DM
                userID = None # plus de mention
                sourceMessage = None # plus de message source
                finalEmbed.add_field(name = "Info", value = "Message envoyé en DM car le salon n'est plus disponible.")
            else:
                sourceMessage = expired[6]
                if sourceMessage != None: # vérification message avec slash command et que si c'est pas en DM
                    try:
                        sourceMessage = await channel.fetch_message(sourceMessage) # récupération message
                    except:
                        sourceMessage = None # message a été supprimé
                    if sourceMessage != None:
                        await sourceMessage.add_reaction(emoji = '✅') # ajout réaction
            finalEmbed.set_footer(text=f"Message d'il y a {timedeltaToString(int(nowUTC()) - expired[3])}")
            links = ""
            findedURLs = getURLsInString(reminder)
            for i in range(0, len(findedURLs)): # ajout de field "lien" pour pouvoir cliquer sur les liens facilement
                links += f"[Lien {i + 1}]({findedURLs[i]}) · "
            if len(findedURLs) > 0:
                finalEmbed.add_field(name = f"Lien{'s' if len(findedURLs) > 1 else ''}", value = links[:-3])
            message = ""
            if userID != None: # metion de l'utilisateur si le message n'est pas en DM
                message = f"<@{userID}>"
            if expired[1] == 1: # s'il faut mentionner les personnes dans le message
                mentionList = getMentionInString(reminder)
                for i in mentionList:
                    message += f" {i}"
            try:
                await channel.send(message, embed = finalEmbed) # envoie du rappel
            except: # les DM sont fermés
                pass
            return Reminder().suppressionReminder(expired[5]) # suppression du rappel
    @_reminderLoop.before_loop
    async def __avant_reminderLoop(self):
        await self.client.wait_until_ready()

    @commands.command(name='reminderlist', aliases=["remindlist", "rl", "rappeliste"])
    async def _reminderlist(self, ctx, *utilisateur):
        """Affiche la liste des rappels d'un utilisateur.⁢⁢⁢⁢⁢\n	➡ Syntaxe: {PREFIX}reminderlist/rl/remindlist/rappeliste [utilisateur]"""
        _, fromSlash, utilisateur = isSlash(utilisateur)
        if len(utilisateur) > 0:
            try:
                utilisateur = mentionToUser(getMentionInString(utilisateur[0])[0])
            except:
                return await mySendHidden(ctx, fromSlash, "L'utilisateur renseigné n'a pas été trouvé.")
        else:
            utilisateur = ctx.author.id

        reminders = Reminder().listeReminder(utilisateur, ctx.guild.id)
        if fromSlash != True:
            await ctx.message.add_reaction(emoji = '✅')
        embed = discord.Embed(description = f"**Rappel{'s' if len(reminders) > 1 else ''} de <@{utilisateur}>**", color = discord.Colour.random())
        embed.set_thumbnail(url = self.client.get_user(utilisateur).avatar_url_as(size = 64))
        if len(reminders) > 0:
            for reminder in reminders:
                texte = reminder[0]
                if len(texte) > 1024:
                    texte = f"{texte[:1021]}..."
                expiration = reminder[2] - int(nowUTC())
                if expiration > 0:
                    expiration = f"Expire dans {timedeltaToString(expiration)} +1m de retard max."
                else:
                    expiration = f"A déjà expiré."
                embed.add_field(value = texte, name = f"#{reminder[3]} • Fais le {timestampScreen(intToDatetime(reminder[1]))}\n{expiration}", inline = False)
        else:
            embed.add_field(name = "\u200b", value = "Vous n'avez aucun rappel en attente !")
        embed.set_footer(text = "Les rappels qui ont déjà expirés vont apparaître dans quelques instants.")
        await ctx.send(embed = embed)
    @cog_ext.cog_slash(name="reminderlist", description = "Affiche la liste des rappels d'un utilisateur.")
    async def __reminderlist(self, ctx, user = None):
        if user == None:
            return await self._reminderlist(ctx, True)
        else:
            return await self._reminderlist(ctx, user, True)

    @commands.command(name='reminderdelete', aliases=["reminddelete", "rd"])
    async def _reminderdelete(self, ctx, *id):
        """Suppprime un rappel.⁢⁢⁢⁢⁢\n	➡ Syntaxe: {PREFIX}reminderdelete/rd <id>"""
        id, fromSlash, _ = isSlash(id)
        if id:
            try:
                id = int(id[0])
            except:
                return await mySendHidden(ctx, fromSlash, "L'ID renseigné n'est pas valide.")
        else:
            return await ctx.send("Veuillez renseigner un ID.")

        verification = Reminder().appartenanceReminder(ctx.author.id, id, ctx.guild.id)
        if verification:
            Reminder().suppressionReminder(id)
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '✅')
            return await ctx.send(f"Reminder **#{id}** supprimé !")
        else:
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '❌')
            return await mySendHidden(ctx, fromSlash, "Rappel non trouvé, pas sur le bon serveur ou qui ne vous appartiens pas.")
    @cog_ext.cog_slash(name="reminderdelete", description = "Suppprime un rappel.")
    async def __reminderdelete(self, ctx, id):
        return await self._reminderdelete(ctx, id, True)

    @commands.command(name='changelogs', aliases=["changelog", "changement", "changements"])
    async def _changelogs(self, ctx, *version):
        """Affiche les changements de la dernière version ou d'une version précise.⁢⁢⁢⁢⁢\n	➡ Syntaxe: {PREFIX}changelogs/changelog/changement/changements [version]"""
        version, fromSlash, _ = isSlash(version)
        if not version:
            version = 'latest'
        changes = getChangelogs(version.replace(',', '.'))
        if changes == None or changes == 0:
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '❌')
            if changes == None:
                message = "Veuillez renseigner un numéro de version valide et existant."
            else:
                message = "Trop de requêtes sur l'API de Github, réessayez plus tard."
            return await mySendHidden(ctx, fromSlash, message)
        if fromSlash != True:
            await ctx.message.add_reaction(emoji = '✅')
        if len(changes[2]) > 2048:
            changes[2] = f"{changes[2][:1900]}..."
        embed = discord.Embed(description = f"[lien vers la page Github]({changes[0]})\n\n{changes[2]}", color = discord.Colour.random())
        embed.set_author(name = f"Changements de la v{changes[1]}")
        await ctx.send(embed = embed)
    @cog_ext.cog_slash(name="changelogs", description = "Affiche les changements de la dernière version ou d'une version précise.")
    async def __changelogs(self, ctx, version = None):
        if version == None:
            return await self._changelogs(ctx, True)
        else:
            return await self._changelogs(ctx, version, True)

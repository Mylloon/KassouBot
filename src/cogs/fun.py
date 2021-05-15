import discord, re
from discord.ext import commands
from random import randint, choice
from datetime import timedelta

def setup(client):
    client.add_cog(Fun(client))

class Fun(commands.Cog):
    """Commandes plutôt fun."""

    def __init__(self, client):
        self.client = client

    @commands.command(name='iq')
    async def _iq(self, ctx, *, user = '0'):
        """Calcule ton IQ.\n	➡ Syntaxe: {PREFIX}iq [user]⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        if user == '0':
            user = ctx.author
            await ctx.message.add_reaction(emoji = '✅')
            return await ctx.send(f"T'as {randint(randint(-100,0),220)} IQ {user.mention} !")
        else:
            try:
                user2 = user
                user2 = user2[2:-1]
                user2 = user2.replace("!","")
                user2 = int(user2)
                user2 = self.client.get_user(user2)
                KassouBot = self.client.get_user(740140888373854269)
                if user2.id == KassouBot.id:
                    await ctx.message.add_reaction(emoji = '✅')
                    return await ctx.send(f"Bah... pas ouf... j'ai juste 100000 IQ :/")
                else:
                    await ctx.message.add_reaction(emoji = '✅')
                    message = await ctx.send("...")
                    return await message.edit(content = f"{user2.mention} a {randint(randint(-100,0),220)} IQ  !")
            except:
                await ctx.message.add_reaction(emoji = '✅')
                message = await ctx.send("...")
                return await message.edit(content = f"{user} a {randint(randint(-100,0),220)} IQ  !")

    @commands.command(name='love')
    async def _love(self, ctx, *users: discord.Member):
        """Découvre la probabilité que ces deux personnes se mettent en couple.\n	➡ Syntaxe: {PREFIX}love <User1> <User2>"""
        if len(users) == 2 or len(users) == 1:
            UneDemande = False
            if len(users) == 1:
                U = users
                users = []
                users.append(U[0])
                users.append(ctx.author)
                UneDemande = True
            if users[0] == users[1]:
                await ctx.message.add_reaction(emoji = '✅')
                return await ctx.send("Je suis sûr que cette personne s'aime ! :angry:")
            if users[0].nick:
                user1 = list(users[0].nick)
            else:
                user1 = list(users[0].name)
            if users[1].nick:
                user2 = list(users[1].nick)
            else:
                user2 = list(users[1].name)
            user1_CALC = self._retirerDoublons([x.lower() for x in user1])
            user2_CALC = self._retirerDoublons([x.lower() for x in user2])
            coef_amour = 0
            if len(user1_CALC) > len(user2_CALC):
                taille_du_pls_grand = len(user1_CALC)
                taille_du_ms_grand = len(user2_CALC)
            else:
                taille_du_pls_grand = len(user2_CALC)
                taille_du_ms_grand = len(user1_CALC)
            coef_amour = round(float(len(list(set(user1_CALC).intersection(user2_CALC))) / taille_du_pls_grand),1) * 100 + ((taille_du_pls_grand-taille_du_ms_grand) * 1.5) * 1.7
            if coef_amour > 100:
                coef_amour = 100
            if UneDemande == True:
                await ctx.message.add_reaction(emoji = '✅')
                return await ctx.send(f"Tu as {coef_amour}% de chance de te mettre en couple avec {''.join(user1)}")
            await ctx.message.add_reaction(emoji = '✅')
            await ctx.send(f"{''.join(user1)} et {''.join(user2)} ont {coef_amour}% de chance de se mettre en couple !")
        else:
            await ctx.message.add_reaction(emoji = '❌')
            await ctx.send(f"Erreur! Syntaxe : `{ctx.prefix}love <User1> [User2]`\n")
    def _retirerDoublons(self, liste):
        Newliste = []
        for element in liste:
            if element not in Newliste:
                Newliste.append(element)
        return Newliste
    @_love.error
    async def _love_error(self, ctx, error):
        await ctx.send(str(error).replace('Member "', "Le membre **").replace('" not found', "** n'as pas été trouvé."))

    @commands.command(name='8ball', aliases=['8b', '8balls'])
    async def _8ball(self, ctx, *, question):
        """Répond à ta question 🔮.\n	➡ Syntaxe: {PREFIX}8ball/8b <question>⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        reponses=["c'est sûr.","il en est décidément ainsi.","incontestablement.","oui sans aucun doute.","tu peux t'y fier.","tel que je le vois, oui.","c'est le plus probable.",
        "cela montre de bonnes perspectives.","certes.","les signes indiquent que oui.","ma réponse est oui.","ta question est trop floue, réessaie.","redemandes plus tard stp.",
        "je ferais mieux de pas te le dire maintenant...","je ne peux pas le prédire actuellement :/","concentre-toi et redemande.","n'y comptes pas trop.","ma réponse est non.",
        "mes sources disent que non.", "les perspectives ne sont pas si bonnes...","c'est très douteux."]
        await ctx.send(f"{ctx.author.mention}, {choice(reponses)}")
    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if str(error) == "question is a required argument that is missing.":
            await ctx.send(f"Mauvaise syntaxe : `{ctx.prefix}8ball/8b/8balls <question>`.")

    @commands.command(name='pileouface', aliases=['pf'])
    async def _pileouface(self, ctx):
        """Pile ou face.\n	➡ Syntaxe: {PREFIX}pileouface/pf"""
        await ctx.message.add_reaction(emoji = '✅')
        return await ctx.send(f"{'Pile' if randint(0,1) == 1 else 'Face'} !")

    @commands.command(name='mock')
    async def _mock(self, ctx):
        """Se moque du message précédent⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        first = 0
        suite_auteur = None
        temps_limite = (await ctx.message.channel.history(limit = 2).flatten())[1].created_at - timedelta(minutes = 5)
        final_message = ""
        async for message in ctx.message.channel.history(limit = 20, after = temps_limite, oldest_first = False):
            if first == 0:
                first = 1
                continue
            if first == 1:
                final_message = message.content
                first = 2
            if suite_auteur:
                if suite_auteur == message.author:
                    final_message = f"{message.content}\n{final_message}"
                    continue
                else:
                    break
            if message.author != ctx.author:
                final_message = message.content
                suite_auteur = message.author
                
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', final_message)
        for i in range (0, len(urls)):
            final_message = final_message.replace(urls[i], '')

        message = []
        message[:0] = final_message.lower()

        for i in range (0, len(message)):
            if randint(0,1) == 1:
                message[i] = message[i].upper()

        await ctx.message.delete()
        if len(message) > 0:
            return await ctx.send("".join(message).replace("\\N", "\n").replace("\\n", "\n"))
        else:
            return await ctx.send("Le message ne contient aucun texte.", delete_after = 5)

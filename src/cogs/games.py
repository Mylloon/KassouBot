import discord
from discord.ext import commands
from random import randint, choice
import asyncio
from discord_slash import cog_ext

def setup(client):
    client.add_cog(Games(client))

class Games(commands.Cog):
    """Commandes relatives aux jeux."""

    def __init__(self, client):
        self.client = client
        self.guessing_game = {}

    @commands.command(name='chifumi', aliases = ["shifumi", "ppc"])
    async def _chifumi(self, ctx, *choix):
        """Un simple Chifumi contre le bot.\n	➡ Syntaxe: {PREFIX}chifumi/shifumi/ppc <pierre/papier/ciseaux>"""
        fromSlash = False
        if len(choix) < 1:
            raise ModuleNotFoundError
        if choix[-1] == True:
            fromSlash = choix[-1]
        choix = choix[0]

        choix_jeu = ["Pierre ✊", "Papier 🧻", "Ciseaux ✂"]
        orditxt = choice(choix_jeu)
        ordi = choix_jeu.index(orditxt)

        PIERRE = 0
        PAPIER = 1
        CISEAUX = 2

        choix = choix.lower()
        if choix == "pierre":
            choix = PIERRE
        if choix == "papier" or choix == "feuille":
            choix = PAPIER
        if choix == "ciseaux" or choix == "ciseau":
            choix = CISEAUX

        description = (f"{choix_jeu[choix][:-1]} VS {choix_jeu[ordi][:-1]}\n\n**"
                       f"{('Égalité !', 'Tu as perdu !', 'Tu as gagné !')[(choix != ordi) + ((choix > ordi and ordi +1 == choix) or (choix < ordi and choix + ordi == 2))]}**")
        
        embed = discord.Embed(title = f"{choix_jeu[choix][-1:]}VS {choix_jeu[ordi][-1:]}", description = description)
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        if fromSlash != True:
            await ctx.message.add_reaction(emoji = '✅')
        return await ctx.send(embed = embed)
    @_chifumi.error
    async def _chifumi_error(self, ctx, error):
        await ctx.send(f"Mauvaise syntaxe : `{ctx.prefix}chifumi/shifumi/ppc <pierre/papier/ciseaux>`.")
    @cog_ext.cog_slash(name="chifumi", description = "Un simple Chifumi contre le bot. <pierre/papier/ciseaux>")
    async def __chifumi(self, ctx, choix):
        return await self._chifumi(ctx, choix, True)

    @commands.command(name='plusoumoins', aliases = ['+ou-', '+-'])
    async def _plusoumoins(self, ctx):
        """Un plus ou moins entre 1 et 100.\n	➡ Syntaxe: {PREFIX}plusoumoins/+ou-/+-⁢⁢⁢⁢⁢"""
        if str(ctx.author.id) in self.guessing_game:
            return await ctx.send("Tu es déjà en partie.")
        guess = 5
        self.guessing_game[str(ctx.author.id)] = guess
        number = randint(1,100)
        message = f"Choisis un nombre entre 1 et 100 {ctx.author.mention}."
        await ctx.send(message)
        while self.guessing_game[str(ctx.author.id)] != 0: 
            try:
                def check(message):
                    if message.author.bot == False:
                        return str(message.author.id) in self.guessing_game
                msg = await self.client.wait_for('message', check = check, timeout = 30)
            except asyncio.TimeoutError:
                del self.guessing_game[str(ctx.author.id)]
                return await ctx.send(f"Tu as mis trop de temps a répondre {ctx.author.mention}. La réponse était {number}.")
            if msg.author == ctx.author:
                if msg.content == "stop":
                    del self.guessing_game[str(ctx.author.id)]
                    return await ctx.send(f"Fin du plus ou moins {ctx.author.mention}. La réponse était {number}.")
                try:
                    attempt = int(msg.content)
                    if attempt > number:
                        if guess-1 != 0:
                            await ctx.send(f"J'pense que c'est moins {ctx.author.mention}... Il te reste {guess-1} essai{'s' if guess-1>1 else ''}.")
                        guess -= 1
                        self.guessing_game[str(ctx.author.id)] = guess
                        if guess != 0:
                            await ctx.send(message)
                    elif attempt < number:
                        if guess-1 != 0:
                            await ctx.send(f"J'pense que c'est plus {ctx.author.mention}... Il te reste {guess-1} essai{'s' if guess-1>1 else ''}.")
                        guess -=1
                        self.guessing_game[str(ctx.author.id)] = guess
                        if guess != 0:
                            await ctx.send(message)
                    elif attempt == number:
                        del self.guessing_game[str(ctx.author.id)]
                        return await ctx.send(f"Tu as trouvé {ctx.author.mention}, bien joué !")
                except:
                    await ctx.send(f"Erreur dans la réponse {ctx.author.mention}, merci de n'écrire qu'un nombre. Tapez `stop` pour arrêter le jeu.")
        del self.guessing_game[str(ctx.author.id)]
        await ctx.send(f"T'as pas trouvé {ctx.author.mention}... dommage, c'était {number}.")

    @commands.command(name='pileouface', aliases=['pf'])
    async def _pileouface(self, ctx, fromSlash = False):
        """Pile ou face.\n	➡ Syntaxe: {PREFIX}pileouface/pf"""
        if fromSlash != True:
            await ctx.message.add_reaction(emoji = '✅')
        return await ctx.send(f"{'Pile' if randint(0,1) == 1 else 'Face'} !")
    @cog_ext.cog_slash(name="pileouface", description = "Pile ou face.")
    async def __pileouface(self, ctx):
        await self._pileouface(ctx, True)

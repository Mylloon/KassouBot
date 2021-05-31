import discord
import feedparser
import os
from discord.ext import commands
from random import choice
from asyncpraw import Reddit
from discord_slash import cog_ext
from utils.core import randomImage

def setup(client):
    client.add_cog(Internet(client))

class Internet(commands.Cog):
    """Commandes relatives à ce qui provient d'internet."""

    def __init__(self, client):
        self.client = client

    @commands.command(name='memes', aliases = ['meme'])
    async def _memes(self, ctx, *args):
        """Envois un meme de reddit.\n	➡ Syntaxe: {PREFIX}memes/meme [subreddit]⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        fromSlash = False
        if len(args) > 0:
            if args[-1] == True:
                fromSlash = args[-1]
                args = args[:-1]
        if len(args) > 0:
            args = args[0]
        else:
            args = None

        if args: # s'il y a un subreddit de défini
            subredditchoix = args
        else: # s'il n'y en a pas
            subredditchoix = choice(['memes', 'anime_irl', 'goodanimemes', 'BikiniclienttomTwitter', 'dankmemes', 'DeepFried',
            'educationalmemes', 'funny', 'marvelmemes', 'me_irl', 'meme', 'MemeEconomy', 'Memes_Of_The_Dank', 'MinecraftMemes',
            'physicsmemes', 'reactiongifs', 'blackpeopletwitter', 'metal_me_irl', 'bee_irl', '195', 'shittyadviceanimals', 'meirl',
            '2meirl4meirl', 'AdviceAnimals', 'weirdmemes'])

        try:
            async with Reddit(client_id = os.environ['TOKEN_REDDIT_CLIENT_ID'], client_secret = os.environ['TOKEN_REDDIT_CLIENT_SECRET'], user_agent = f"disreddit /u/{os.environ['TOKEN_REDDIT_USER_AGENT']}, http://localhost:8080") as reddit:
                subreddit = await reddit.subreddit(subredditchoix) # récupération du subreddit
                hot = subreddit.top(limit = 20) # récupération des memes avec une limite aux 10 premiers memes
                all_subs = [item async for item in hot] # liste des memes
                submission = choice(all_subs) # choix aléatoire

            image = ["png", "jpg", "jpeg", "bmp", "gif"]
            if submission.url[-3:] in image:
                embed = discord.Embed(title = f"r/{subredditchoix} pour {ctx.author.name}", color = discord.Colour.random(), description = f"[lien du meme]({submission.url})")
                embed.set_footer(text = f"Meme de Reddit")
                embed.set_image(url = submission.url)
                message = await ctx.send(embed = embed)
            else:
                await ctx.send(f"```r/{subredditchoix} pour {ctx.author.name}```\n{submission.url}")
                message = await ctx.send("```Meme de Reddit```")
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '✅')
            await message.add_reaction('👍')
            return await message.add_reaction('👎')

        except Exception as error:
            print(f"Error in _memes command = args: {args}, subreddit: {subredditchoix}, error: {error}")
            await ctx.message.add_reaction(emoji = '❌')
            return await ctx.send(f"Ce subreddit est interdit, mis en quarantaine ou n'existe pas. ({subredditchoix})")
    @cog_ext.cog_slash(name="meme", description = "Envois un meme de reddit.")
    async def __memes(self, ctx, subreddit = None):
        if subreddit == None:
            return await self._memes(ctx, True)
        else:
            return await self._memes(ctx, subreddit, True)

    @commands.command(name='cat', aliases = ['chat'])
    async def _cat(self, ctx, fromSlash = False):
        """Te montre un magnifique chat.\n	➡ Syntaxe: {PREFIX}cat/chat"""

        if ctx.author.nick:
            name =  f"{ctx.author.nick} ({ctx.author.name}#{ctx.author.discriminator})"
        else:
            name = f"{ctx.author.name}"
        embed = discord.Embed(title = f"Poticha pour {name}", colour = discord.Colour.random())
        cat = randomImage("http://aws.random.cat/meow")
        embed.set_image(url = cat[0]['file'])
        embed.set_footer(text = f"random.cat a pris {cat[1]} ms.")
        if fromSlash != True:
            await ctx.message.add_reaction(emoji = '✅')
        message = await ctx.send(embed=embed)
        return await message.add_reaction('❤️')
    @cog_ext.cog_slash(name="cat", description = "Te montre un magnifique chat.")
    async def __cat(self, ctx):
        return await self._cat(ctx, True)

    @commands.command(name='dog', aliases = ['chien'])
    async def _dog(self, ctx, fromSlash = None):
        """Te montre un magnifique chien.\n	➡ Syntaxe: {PREFIX}dog/chien"""
        if fromSlash == None:
            fromSlash = False

        if ctx.author.nick:
            name =  f"{ctx.author.nick} ({ctx.author.name}#{ctx.author.discriminator})"
        else:
            name = f"{ctx.author.name}"
        embed = discord.Embed(title = f"Potichien pour {name}", colour = discord.Colour.random())
        dog = randomImage("https://dog.ceo/api/breeds/image/random")
        embed.set_image(url = dog[0]['message'])
        embed.set_footer(text = f"dog.ceo a pris {dog[1]} ms.")
        if fromSlash != True:
            await ctx.message.add_reaction(emoji = '✅')
        message = await ctx.send(embed=embed)
        return await message.add_reaction('❤️')
    @cog_ext.cog_slash(name="dog", description = "Te montre un magnifique chien.")
    async def __dog(self, ctx):
        return await self._dog(ctx, True)

    @commands.command(name='sexe', aliases=['sexes', 'nude', 'nudes', 'nsfw'])
    async def _sexe(self, ctx, *choice_of_nsfw):
        """Envois une image coquine. (NSFW)\n	➡ Syntaxe: {PREFIX}sexe/sexes/nude/nudes [butts/boobs]⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        fromSlash = False
        if len(choice_of_nsfw) > 0:
            if choice_of_nsfw[-1] == True:
                fromSlash = choice_of_nsfw[-1]
                choice_of_nsfw = choice_of_nsfw[:-1]
        if len(choice_of_nsfw) > 0:
            choice_of_nsfw = choice_of_nsfw[0]
        else:
            choice_of_nsfw = None

        liste_hot = ['butts', 'boobs']
        if choice_of_nsfw == 'butt':
            choice_of_nsfw = 'butts'
        if choice_of_nsfw == 'boob':
            choice_of_nsfw = 'boobs'
        if choice_of_nsfw in liste_hot:
            pass
        else:
            choice_of_nsfw = choice(liste_hot)
        if ctx.channel.is_nsfw():
            embed = discord.Embed(title = f"{choice_of_nsfw.capitalize()} pour {ctx.author.name}", colour = discord.Colour.random())
            nsfw = randomImage(f'http://api.o{choice_of_nsfw}.ru/noise/')
            print(nsfw)
            embed.set_image(url = f"http://media.o{choice_of_nsfw}.ru/{nsfw[0][0]['preview']}")
            embed.set_footer(text = f"o{choice_of_nsfw}.ru a pris {nsfw[1]} ms pour sortir l'image n°{nsfw[0][1]}-{nsfw[1]}.")
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '✅')
            await ctx.send(embed = embed)
        else:
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '❌')
            await ctx.send(f"Désolé mais je n'envois ce genre de message seulement dans les salons NSFW !")
    @cog_ext.cog_slash(name="sexe", description = "Envois une image coquine. (NSFW)")
    async def __sexe(self, ctx, buttsorboobs = None):
        if buttsorboobs == None:
            return await self._sexe(ctx, True)
        else:
            return await self._sexe(ctx, buttsorboobs, True)

    @commands.command(name='news', aliases=['rss'])
    async def _news(self, ctx, *arg):
        """Info random dans le domaine de l'informatique\n	➡ Syntaxe: {PREFIX}news/rss [site/liste]"""
        fromSlash = False
        if len(arg) > 0:
            if arg[-1] == True:
                fromSlash = arg[-1]
                arg = arg[:-1]
        if len(arg) > 0:
            arg = arg[0]
        else:
            arg = ""

        rss_website = {
            "anandtech": "https://www.anandtech.com/rss/",
            "arstechnica": "https://arstechnica.com/feed",
            "certssi": "https://www.cert.ssi.gouv.fr/feed/",
            "frenchlegion": "http://frenchlegion.eu/feed/",
            "guru3d": "https://www.guru3d.com/news_rss",
            "hardwareleaks": "https://hardwareleaks.com/feed",
            "lesnumeriques": "https://www.lesnumeriques.com/rss.xml",
            "overclock3d": "https://www.overclock3d.net/xmlfeed",
            "overclocking": "https://overclocking.com/feed/",
            "pcper": "https://pcper.com/feed",
            "rtings": "https://www.rtings.com/reviews-rss.xml",
            "storagereview": "https://www.storagereview.com/feed",
            "techpowerupnews": "https://www.techpowerup.com/rss/news",
            "techpowerupreviews": "https://www.techpowerup.com/rss/reviews",
            "techspot": "https://www.techspot.com/backend.xml",
            "videocardz": "https://videocardz.com/feed",
            "vonguru": "https://vonguru.fr/feed/"
        }

        choix_site = choice([key for key in rss_website.keys()])
        
        if arg.lower() in rss_website: # si on specifie la source
            choix_site = arg.lower()

        if arg.lower() == "liste":
            embed = discord.Embed(title = "Liste des sources", color = discord.Colour.random(), description = ", ".join([key.capitalize() for key in rss_website.keys()]))
            return await ctx.send(embed = embed)

        newsfeed = feedparser.parse(rss_website[choix_site])
        info = choice([newsfeed.entries[i] for i in range(0, 10 if len(newsfeed.entries) > 10 else len(newsfeed.entries))])

        desc = "Pas de description trouvée." if "<p>" in info.description or "</a>" in info.description else info.description
        embed = discord.Embed(title = info.title, color = discord.Colour.random(), description = f"[**lien de la news**]({info.link})\n\n{desc}")
        try:
            embed.set_author(name = info.author)
        except:
            pass
        embed.set_footer(text = f"News de {choix_site.capitalize()}")
        await ctx.send(embed = embed)
        if fromSlash != True:
            await ctx.message.add_reaction(emoji = '✅')
    @cog_ext.cog_slash(name="news", description = "Info random dans le domaine de l'informatique, met commme arg liste pour la liste des sources dispo.")
    async def __news(self, ctx, source = None):
        if source == None:
            return await self._news(ctx, True)
        else:
            return await self._news(ctx, source, True)

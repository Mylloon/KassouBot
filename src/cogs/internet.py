import discord
from feedparser import parse
from os import environ
from discord.ext import commands
from random import choice
from asyncpraw import Reddit
from discord_slash import cog_ext
from utils.core import randomImage, isSlash, mySendHidden

def setup(client):
    client.add_cog(Internet(client))

class Internet(commands.Cog):
    """Commandes relatives à ce qui provient d'internet."""
    def __init__(self, client):
        self.client = client

    @commands.command(name='memes', aliases = ['meme'])
    async def _memes(self, ctx, *args):
        """Envoie un meme de reddit.\n	➡ Syntaxe: {PREFIX}memes/meme [subreddit]⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        args, fromSlash, _ = isSlash(args)

        if args: # s'il y a un subreddit de défini
            subredditchoix = args
        else: # s'il n'y en a pas
            subredditchoix = choice(['memes', 'goodanimemes', 'dankmemes', 'DeepFried',
            'educationalmemes', 'funny', 'marvelmemes', 'me_irl', 'meme', 'MemeEconomy', 'Memes_Of_The_Dank', 'MinecraftMemes',
            'physicsmemes', 'blackpeopletwitter', 'metal_me_irl', '195', 'shittyadviceanimals', 'meirl',
            '2meirl4meirl', 'AdviceAnimals', 'weirdmemes', 'LeagueOfMemes'])
        
        if fromSlash != None and subredditchoix == "nsfw": # demande de nsfw sans passé par la commande appropriée
            return await mySendHidden(ctx, fromSlash, f"Désolé, tu demandes du nsfw... Fais plutôt **{ctx.prefix}sexe**.")

        try:
            async with Reddit(client_id = environ['TOKEN_REDDIT_CLIENT_ID'], client_secret = environ['TOKEN_REDDIT_CLIENT_SECRET'], user_agent = f"disreddit /u/{environ['TOKEN_REDDIT_USER_AGENT']}, http://localhost:8080") as reddit:
                subreddit = await reddit.subreddit(subredditchoix) # récupération du subreddit
                hot = subreddit.top(limit = 20) # récupération des memes avec une limite aux 10 premiers memes
                all_subs = [item async for item in hot] # liste des memes
                submission = choice(all_subs) # choix aléatoire

            image = ["png", "jpg", "jpeg", "bmp", "gif"] # gifv not working
            if submission.url[-3:] in image:
                if fromSlash != None:
                    footer = "Meme de Reddit"
                    memeOuImage = "[lien du meme]"
                else:
                    footer = "NSFW de Reddit"
                    memeOuImage = "[lien de l'image]"
                embed = discord.Embed(title = f"r/{subredditchoix} pour {ctx.author.name}", color = discord.Colour.random(), description = f"{memeOuImage}({submission.url})")
                embed.set_footer(text = footer)
                embed.set_image(url = submission.url)
                message = await ctx.send(embed = embed)
            else:
                if fromSlash != None:
                    message = await ctx.send(f"`r/{subredditchoix} pour {ctx.author.name}`\n{submission.url}")
                else:
                    message = await ctx.send(f"`{subredditchoix.capitalize()} pour {ctx.author.name}`\n{submission.url}")
            if fromSlash != True and fromSlash != None:
                await ctx.message.add_reaction(emoji = '✅')
            if fromSlash != None:
                for emoji in ['🔺', '🔻']:
                    await message.add_reaction(emoji)

        except Exception as error:
            print(f"Error in _memes command = args: {args}, subreddit: {subredditchoix}, error: {error}")
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '❌')
            return await mySendHidden(ctx, fromSlash, f"Ce subreddit est interdit, mis en quarantaine ou n'existe pas. ({subredditchoix})")
    @cog_ext.cog_slash(name="meme", description = "Envoie un meme de reddit.")
    async def __memes(self, ctx, subreddit = None):
        ctx.prefix = "/"
        if subreddit == None:
            return await self._memes(ctx, True)
        else:
            return await self._memes(ctx, subreddit, True)

    @commands.command(name='cat', aliases = ['chat'])
    async def _cat(self, ctx, fromSlash = None):
        """Te montre un magnifique chat.\n	➡ Syntaxe: {PREFIX}cat/chat"""
        if fromSlash != True:
            fromSlash = False

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
        if fromSlash != True:
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
    async def _sexe(self, ctx, fromSlash = None):
        """Envois une image coquine. (NSFW)\n	➡ Syntaxe: {PREFIX}sexe/sexes/nude/nudes"""
        if fromSlash != True:
            fromSlash = False
        if ctx.channel.is_nsfw():
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '✅')
            else:
                ctx.prefix = "/"
            return await self._memes(ctx, "nsfw", None)
        else:
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '❌')
            await mySendHidden(ctx, fromSlash, f"Désolé mais je n'envois ce genre de message seulement dans les salons NSFW !")
    @cog_ext.cog_slash(name="sexe", description = "Envois une image coquine. (NSFW)")
    async def __sexe(self, ctx):
        return await self._sexe(ctx, True)

    @commands.command(name='news', aliases=['rss'])
    async def _news(self, ctx, *arg):
        """Info random dans le domaine de l'informatique\n	➡ Syntaxe: {PREFIX}news/rss [site/liste]"""
        arg, fromSlash, _ = isSlash(arg)
        if arg == None:
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

        newsfeed = parse(rss_website[choix_site])
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

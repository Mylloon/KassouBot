import discord, praw, json, requests, time, feedparser
from discord.ext import commands
from random import randint, choice
from tokens import token_reddit as token # à l'importation de l'extension, le fichier se retrouve dans le '/' et non dans 'cogs/', ignorez l'erreur pylint

def setup(client):
    client.add_cog(Internet(client))

class Internet(commands.Cog):
    """Commandes relatives à ce qui provient d'internet."""


    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 770805818487865404 or message.channel.id == 772239638240165928: # Le groupe de l'amour ❤❤ -- channel chien/chat
            chiens = ["dog", "chien", "potichien"]
            chats = ["kat", "mace", "kater", "katze", "sinta", "minoos", "cat", "qitt", "besseh", "katu", "caun", "kazh",
            "bisig", "moggy", "kotka", "maow", "gat", "we'sa", "guigna", "kodkod", "mao", "koyangi", "ghjattu", "míw", "pussi",
            "gato", "gata", "kato", "kass", "domadh", "demmat", "kissa", "chat", "minou", "piscín", "cath", "k'at'a", "muca", "gali",
            "gatos", "popoki", "kike", "chatul", "chatula", "billa", "kat poes", "macska", "cica", "kutjing", "kucing", "köttur",
            "gatto", "gattina", "neko", "chma", "pising", "feles", "felix", "kakis", "katé", "qattus", "qattusa", "ngeru", "miz", "felino",
            "felina", "muur", "katt", "shimii", "billi", "gorbe", "pusa", "kot", "giat", "pisica", "koshka", "pusi", "macka", "mizhu",
            "kotsur", "bisad", "büsi", "chatz", "paka", "muc", "poonai", "puunay", "kocour", "kocka", "maa-oh", "kedi", "kit", "con mêo",
            "tchèt", "mouss", "ologbo", "kats", "猫", "кот", "고양이", "poticha", "😼", "ʇɐɥɔ"]
            if message.content.lower() in chiens:
                await self._dog(await self.client.get_context(message))
            if message.content.lower() in chats:
                await self._cat(await self.client.get_context(message))

    @commands.command(name='memes', aliases = ['meme'])
    async def _memes(self, ctx, *, args = ""):
        """Envois un meme de reddit.\n	➡ Syntaxe: .memes/meme [subreddit]⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        try:
            reddit = praw.Reddit(client_id = token['client_id'], client_secret = token['client_secret'], user_agent = f"disreddit /u/{token['user_agent']}, http://localhost:8080")

            if args != "": # si il y a un arg différent d'un meme
                subredditchoix = args

            else: # si il n'y a pas d'arguments
                subredditchoix = choice(['memes', 'anime_irl', 'goodanimemes', 'BikiniclienttomTwitter', 'dankmemes', 'DeepFriedMemes',
                'educationalmemes', 'funny', 'marvelmemes', 'me_irl', 'meme', 'MemeEconomy', 'Memes_Of_The_Dank', 'MinecraftMemes',
                'physicsmemes', 'reactiongifs', 'blackpeopletwitter', 'metal_me_irl', 'bee_irl', '195',
                'shittyadviceanimals', 'meirl', '2meirl4meirl', 'AdviceAnimals', 'weirdmemes'])

            memes_submissions = reddit.subreddit(subredditchoix).hot()
            post_to_pick = randint(1, 10)
            for i in range(0, post_to_pick): # i pas important
                i = i #retire l'erreur sur vscode
                submission = next(x for x in memes_submissions if not x.stickied)

            image = ["png", "jpg", "jpeg", "bmp", "gif"]
            if submission.url[-3:] in image:
                embed = discord.Embed(title = f"r/{subredditchoix} pour {ctx.author.name}", color = discord.Colour.random(), description = f"[lien du meme]({submission.url})")
                embed.set_footer(text = f"Meme de Reddit")
                embed.set_image(url = submission.url)
                message = await ctx.send(embed = embed)
            else:
                await ctx.send(f"```r/{subredditchoix} pour {ctx.author.name}```\n{submission.url}")
                message = await ctx.send("```Meme de Reddit```")
            await ctx.message.add_reaction(emoji = '✅')
            await message.add_reaction('👍')
            return await message.add_reaction('👎')

        except Exception as error:
            print(f"args: {args}, subreddit: {subredditchoix}, error: {error}")
            await ctx.message.add_reaction(emoji = '❌')
            return await ctx.send(f"Ce subreddit est interdit, mis en quarantaine ou n'existe pas. ({subredditchoix})")

    def _random_image(self, link):
        temps_requete = int(round(time.time() * 1000))
        try:
            request_data = requests.get(link)
        except Exception as e:
            raise Exception(f"Une erreur s'est produite lors de la tentative de demande de l'API {link} : {e}")

        if not request_data.status_code == 200:
            raise Exception(f"Code HTTP {request_data.status_code} au lieu de HTTP 200 à l'appel de {link} : {request_data.text}")

        try:
            json_data = json.loads(request_data.text)
        except Exception as e:
            raise Exception(f"Erreur lors de la transformation les données de {link} en json : {e}")

        temps_requete = int(round(time.time() * 1000)) - temps_requete
        return (json_data, temps_requete)

    @commands.command(name='cat', aliases = ['chat'])
    async def _cat(self, ctx):
        """Te montre un magnifique chat\n	➡ Syntaxe: .cat/chat"""

        if ctx.author.nick:
            name =  f"{ctx.author.nick} ({ctx.author.name}#{ctx.author.discriminator})"
        else:
            name = f"{ctx.author.name}"
        embed = discord.Embed(title = f"Poticha pour {name}", colour = discord.Colour.random())
        cat = self._random_image("http://aws.random.cat/meow")
        embed.set_image(url = cat[0]['file'])
        embed.set_footer(text = f"random.cat a pris {cat[1]} ms.")
        await ctx.message.add_reaction(emoji = '✅')
        message = await ctx.send(embed=embed)
        return await message.add_reaction('❤️')

    @commands.command(name='dog', aliases = ['chien'])
    async def _dog(self, ctx):
        """Te montre un magnifique chien\n	➡ Syntaxe: .dog/chien"""

        if ctx.author.nick:
            name =  f"{ctx.author.nick} ({ctx.author.name}#{ctx.author.discriminator})"
        else:
            name = f"{ctx.author.name}"
        embed = discord.Embed(title = f"Potichien pour {name}", colour = discord.Colour.random())
        dog = self._random_image("https://dog.ceo/api/breeds/image/random")
        embed.set_image(url = dog[0]['message'])
        embed.set_footer(text = f"dog.ceo a pris {dog[1]} ms.")
        await ctx.message.add_reaction(emoji = '✅')
        message = await ctx.send(embed=embed)
        return await message.add_reaction('❤️')

    @commands.command(name='sexe', aliases=['sexes', 'nude', 'nudes', 'nsfw'])
    async def _sexe(self, ctx, *, choice_of_nsfw = None):
        """Envois une image coquine. (NSFW)\n	➡ Syntaxe: .sexe/sexes/nude/nudes [butts/boobs]⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        liste_hot = ['butts', 'boobs']
        if choice_of_nsfw in liste_hot:
            pass
        else:
            choice_of_nsfw = choice(liste_hot)
        if ctx.channel.is_nsfw():
            embed = discord.Embed(title = f"{choice_of_nsfw.capitalize()} pour {ctx.author.name}", colour = discord.Colour.random())
            nsfw = self._random_image(f'http://api.o{choice_of_nsfw}.ru/noise/')
            embed.set_image(url = f"http://media.o{choice_of_nsfw}.ru/{nsfw[0][0]['preview']}")
            embed.set_footer(text = f"o{choice_of_nsfw}.ru a pris {nsfw[1]} ms.")
            await ctx.message.add_reaction(emoji = '✅')
            await ctx.send(embed = embed)
        else:
            await ctx.message.add_reaction(emoji = '❌')
            await ctx.send(f"Désolé mais je n'envois ce genre de message seulement dans les salons NSFW !")

    @commands.command(name='news', aliases=['rss'])
    async def _news(self, ctx, *, arg = ""):
        """Info random dans le domaine de l'informatique\n	➡ Syntaxe: .news/rss [site/liste]"""

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
        await ctx.message.add_reaction(emoji = '✅')

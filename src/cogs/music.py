# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Valentin B.

https://gist.github.com/vbe0201/ade9b80f2d3b64643d854938d40a0a2d
"""

import asyncio
import functools
import itertools
import math
import random

import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands

# Genius API
import lyricsgenius
import time
from tokens import token_genius as token # à l'importation de l'extension, music.py se retrouve dans le '/' et non dans 'cogs/', ignorez l'erreur
genius = lyricsgenius.Genius(token)

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''

def setup(client):
    client.add_cog(Music(client))

class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return f"**{self.title}** de **{self.uploader}**"

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError(f"Je n'ai rien trouvé qui corresponde à `{search}`")

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError(f"Je n'ai rien trouvé qui corresponde à `{search}`")

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError(f"Impossible d'obtenir `{webpage_url}`")

        if "entries" not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError(f"Aucune correspondances pour `{webpage_url}`")

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append(f"{days} jours,{'' if days <= 1 else 's'}")
        if hours > 0:
            duration.append(f"{hours} H,{'' if hours <= 1 else 's'}")
        if minutes > 0:
            duration.append(f"{minutes} min{'' if minutes <= 1 else 's'}")
        if seconds > 0:
            duration.append(f"{seconds} sec{'' if seconds <= 1 else 's'}")

        return ' '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title="Joue",
                               description=f"\n[{self.source.title}]({self.source.url})\n",
                               color=discord.Colour.random())
                 .add_field(name="Durée", value=self.source.duration)
                 .add_field(name="Demandé par", value=self.requester.mention)
                 .add_field(name="Chaîne", value=f"[{self.source.uploader}]({self.source.uploader_url})")
                 .set_thumbnail(url=self.source.thumbnail))

        return embed

    def title(self):
        return self.source.title


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return iter(self._queue.__iter__())

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, client: commands.bot, ctx: commands.Context):
        self.client = client
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 1.0

        self.audio_player = client.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.client.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    """Commandes relatives à la musique - © vbe0201."""
    def __init__(self, client: commands.bot):
        self.client = client
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.client, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.client.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage("Je ne fais pas de musiques en DM.")

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send(f"Une erreur est survenue : {str(error)}")

    @commands.command(name='join', aliases=['j'], invoke_without_subcommand=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """Se connecte au salon vocal.\n	➡ Syntaxe: .connect/join⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""

        if not channel and not ctx.author.voice:
            await ctx.send("Aucun channel à rejoindre. Connecte toi dans un vocal ou donne-moi son id.")
            raise VoiceError("Vous n'êtes pas connecté à un channel vocal et n'avez spécifié aucun channel à rejoindre.")

        destination = channel or ctx.author.voice.channel
        await ctx.send(f":thumbsup: **Connecté à __{destination}__**")
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='stop', aliases=['disconnect', 'dc'])
    async def _leave(self, ctx: commands.Context):
        """Arrête la chanson en cours de lecture et quitte le salon vocal.\n	➡ Syntaxe: .disconnect/dc/stop⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""

        if not ctx.voice_state.voice:
            embed = discord.Embed(description = "Tape `.play <chanson>` pour jouer quelque chose ou `.join [id]` pour me connecter à un salon vocal.", color = 0xC41B1B)
            embed.set_author(name = "Je ne suis connecté à aucun vocal.")
            return await ctx.send(embed = embed)

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]
        await ctx.send("📭 **Déconnecté du salon**")

    @commands.command(name='volume', aliases=['vol'])
    async def _volume(self, ctx: commands.Context, *, volume: int = False):
        """Modifie le volume du bot (entre 1 et 100).\n	➡ Syntaxe: .volume/vol [1;100]⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""

        if not ctx.voice_state.is_playing:
            return await ctx.send("Rien n'est joué pour le moment.")

        if not volume:
            return await ctx.send(f"Le volume est à **{ctx.voice_state.volume * 100}%**")

        if 0 > volume > 100:
            return await ctx.send("Le volume doit être compris entre 0 et 100.")

        ctx.voice_state.volume = volume / 100
        await ctx.send(f"Volume réglé sur **{volume}%**")

    @commands.command(name='now', aliases=['current', 'playing', 'np'])
    async def _now(self, ctx: commands.Context):
        """Affiche des informations sur la chanson en cours de lecture.\n	➡ Syntaxe: .now/current⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢/playing/np"""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    async def _pause(self, ctx: commands.Context):
        """Mets en pause de la chanson en cours de lecture.⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""

        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')
            await ctx.send(f"**`{ctx.author}`** met en pause la chanson en cours.")
        else:
            embed = discord.Embed(description = "Tape `.play <chanson>` pour jouer quelque chose.", color = 0xC41B1B)
            embed.set_author(name = "Je ne joue rien en ce moment !")
            return await ctx.send(embed = embed)

    @commands.command(name='resume')
    async def _resume(self, ctx: commands.Context):
        """Reprends la chanson en pause."""

        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')
            await ctx.send(f"**`{ctx.author}`** relance la chanson.")
        else:
            if ctx.voice_state.is_playing:
                embed = discord.Embed(description = "Tape `.pause` pour mettre en pause la chanson.", color = 0xC41B1B)
                embed.set_author(name = "Je suis déjà en lecture !")
                return await ctx.send(embed = embed)
            else:
                embed = discord.Embed(description = "Tape `.play <chanson>` pour jouer quelque chose ou `.join [id]` pour me connecter à un salon vocal.", color = 0xC41B1B)
                embed.set_author(name = "Je ne suis connecté à aucun vocal.")
                return await ctx.send(embed = embed)

    @commands.command(name='skip', aliases=['s'])
    async def _skip(self, ctx: commands.Context):
        """Passe la chanson.\n	➡ Syntaxe: .skip/s"""

        if not ctx.voice_state.is_playing:
            embed = discord.Embed(description = "Tape `.play <chanson>` pour jouer quelque chose.", color = 0xC41B1B)
            embed.set_author(name = "Je ne joue rien en ce moment !")
            return await ctx.send(embed = embed)
        
        await ctx.message.add_reaction('⏭')
        ctx.voice_state.skip()
        await ctx.send(f"**`{ctx.author}`**: Passe la chanson !")

    @commands.command(name='queue', aliases=['q', 'playlist'])
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Affiche la file d'attente des chansons à venir.\n	➡ Syntaxe: .queue/q⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢/playlist [page]"""

        if len(ctx.voice_state.songs) == 0:
            embed = discord.Embed(description = "Tape `.play <chanson>` pour jouer quelque chose.", color = 0xC41B1B)
            embed.set_author(name = "Il n'y a plus de chanson à venir dans la playlist.")
            return await ctx.send(embed = embed)

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        if page > pages:
            embed = discord.Embed(description = "Tape `.play <chanson>` pour rajouter encore de la musique.", color = 0xC41B1B)
            embed.set_author(name = "Il n'y a pas autant de pages")
            return await ctx.send(embed = embed)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += f"`{i + 1}.` [**{song.source.title}**]({song.source.url})\n"

        embed = (discord.Embed(description=f"**{len(ctx.voice_state.songs)} piste{'s' if len(ctx.voice_state.songs)>1 else ''} :**\n\n{queue}", color = discord.Colour.random())
                 .set_footer(text=f"Page {page}/{pages}"))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        """Mélange la file d'attente."""

        if len(ctx.voice_state.songs) == 0:
            embed = discord.Embed(description = "Tape `.play <chanson>` pour jouer quelque chose.", color = 0xC41B1B)
            embed.set_author(name = "La file est vide.")
            return await ctx.send(embed = embed)

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        """Supprime une chanson de la file d'attente."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("File vide.")

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')
        await ctx.send("Chanson sélectionnée supprimée de la file d'attente.")

    @commands.command(name='loop', aliases=['repeat'])
    async def _loop(self, ctx: commands.Context):
        """Répète la chanson actuellement en lecture.\n	➡ Syntaxe: .loop/repeat"""

        if not ctx.voice_state.is_playing:
            embed = discord.Embed(description = "Tape `.play <chanson>` pour jouer quelque chose.", color = 0xC41B1B)
            embed.set_author(name = "Je ne joue rien en ce moment !")
            return await ctx.send(embed = embed)

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')
        await ctx.send("La chanson change d'état.")

    @commands.command(name='play', aliases=['p'])
    async def _play(self, ctx: commands.Context, *, search: str):
        """Recherche une chanson sur les sites compatibles avec YoutubeDL si aucun URL n'est donné et l'ajoute à la file d'attente.\n	➡ Syntaxe: .play/p⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""

        if not ctx.voice_state.voice:
            await ctx.invoke(self._summon)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.client.loop)
            except YTDLError as e:
                await ctx.send(f"Une erreur s'est produite lors du traitement de cette demande : {str(e)}")
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send(f"En file d'attente {str(source)}")

    @_summon.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError("Vous n'êtes connecté à aucun channel vocal.")

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError("Le bot est déjà dans un channel vocal.")

    @commands.command(name='lyrics', aliases = ['l', 'lyric'])
    async def _lyrics(self, ctx, *, song: str = None):
        """Affiche les paroles de la musique en cours, ou de la chanson spécifiée.\n	➡ Syntaxe: .lyrics/lyric/l (musique)⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        if song or ctx.voice_state.is_playing:
            if not song:
                song = f"{ctx.voice_state.current.title()}"
            if " romanized" in song:
                message = await ctx.send(f":mag: **Cherche les paroles romanisées de ** `{song.replace(' romanized', '')}`")
            else:
                message = await ctx.send(f":mag: **Cherche les paroles de ** `{song}`")
            temps_requete = int(round(time.time() * 1000))
            song_genius = genius.search_song(song)
            couleur_embed = discord.Colour.random()
            try:
                paroles = song_genius.lyrics
            except:
                await ctx.message.add_reaction(emoji = '❌')
                return await message.edit(content = f"Pas de résultats trouvés pour `{song}`.") 
            lignetotal = ""
            premierembed = True
            if len(paroles) > 7500:
                await ctx.message.add_reaction(emoji = '❌')
                return await message.edit(content = f"Désolé, les paroles sont trop longues pour être affichés (lien vers la page des paroles : {song_genius.url}).")
            title_first_embed = f"Paroles de {song_genius.title} par {song_genius.artist}."
            desc_first_embed = f"[Lien vers les paroles sur le site]({song_genius.url})"
            type_de_comptage = "\n\n" if paroles.count("\n\n") > 2 else "\n"
            for ligne in paroles.split(type_de_comptage):
                if len(ligne) >= 2048:
                    type_de_comptage = "\n"
            for ligne in paroles.split(type_de_comptage):
                if len(f"{lignetotal}{type_de_comptage}{ligne}") < 1900:
                    lignetotal = f"{lignetotal}{type_de_comptage}{self.ligne_formatage(ligne)}"
                else:
                    if premierembed == True:
                        premierembed = False
                        embed = discord.Embed(title = title_first_embed, description = f"{desc_first_embed}{lignetotal}", color = couleur_embed)
                        embed.set_thumbnail(url = song_genius.song_art_image_url)
                        await message.edit(embed = embed)
                    else:
                        embed = discord.Embed(description = lignetotal, color = couleur_embed)
                        await ctx.send(embed = embed)
                    lignetotal = f"{self.ligne_formatage(ligne)}"
            
            temps_requete = int(round(time.time() * 1000)) - temps_requete
            footer_embed = f"Pour {self.user_or_nick(ctx.author)} par Genius en {round(temps_requete / 1000, 2)} s."
            await ctx.message.add_reaction(emoji = '✅')
            if premierembed == True:
                premierembed = False
                embed = discord.Embed(title = title_first_embed, description = f"{desc_first_embed}{lignetotal}", color = couleur_embed)
                embed.set_footer(icon_url = ctx.author.avatar_url, text = footer_embed)
                return await message.edit(embed = embed)
            else:
                embed = discord.Embed(description = lignetotal, color = couleur_embed)
                embed.set_footer(icon_url = ctx.author.avatar_url, text = footer_embed)
                return await ctx.send(embed = embed)
        else:
            await ctx.message.add_reaction(emoji = '❌')
            await ctx.send("Aucune musique demandé... `.lyrics/l/lyrics <song>`.")
    def ligne_formatage(self, ligne):
        liste_balise = [
            ('[Hook', '[Accroche'), ('[Verse', '[Couplet'), ('[Chorus', '[Chœur'),
            ('[Bridge', '[Pont'),('[Pre-Chorus', '[Pré-chœur'), ('[Post-Chorus', '[Post-chœur')
        ]
        for balises in liste_balise:
            ligne = ligne.replace(balises[0], balises[1])
        return ligne
    def user_or_nick(self, user):
        if user.nick:
            return f"{user.nick} ({user.name}#{user.discriminator})"
        else:
            return f"{user.name}#{user.discriminator}"

    @commands.command(name='lyricsromanized', aliases = ['lr', 'lyricromanized'], hidden = True)
    async def _lyricsromanized(self, ctx, *, song: str = None):
        await ctx.invoke(self.client.get_command("lyrics"), song = f"{song} romanized" if song else song)

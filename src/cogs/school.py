import discord
from discord.ext import commands

def setup(client):
    client.add_cog(School(client))

class School(commands.Cog):
    """Commandes relatives aux cours."""

    def __init__(self, client):
        self.client = client

    @commands.command(name='appel')
    # @commands.has_any_role("Professeur", "professeur", "Prof", "prof")
    async def _appel(self, ctx, *, voice_channel: int = None):
        """Fais l'appel.⁢⁢⁢⁢⁢\n	➡ Syntaxe: .appel [ID salon vocal]"""
        voice_channels = []
        voice_channels.extend(ctx.guild.voice_channels)
        await ctx.message.add_reaction(emoji = "✅")
        limite_voice_channels = 7
        if len(voice_channels) > limite_voice_channels:
            return await ctx.send(f"""Désolé mais il y a plus de {limite_voice_channels} salons vocaux sur ce serveur, utilisez plutôt `{ctx.prefix}appel {{ID salon vocal}}`.
            \nPour savoir comment récuperer l'id d'un salon vous pouvez faire `{ctx.prefix}getid`.""")
        if voice_channel:
            canal = self.client.get_channel(voice_channel)
            if canal.type.__str__() == "voice":
                voice_channels = [canal]
            else:
                return await ctx.send("Tu as spécifié un channel textuelle et non vocal.")
        if len(voice_channels) > 0:
            embed = discord.Embed(title = "Réagissez à ce message avec ✋ pour signaler votre présence.", description = f"(attention, je réagis aussi) — Professeur : {ctx.author.mention}")
            for channel in voice_channels:
                prof = []
                for role in ["Professeur", "professeur", "Prof", "prof"]:
                    role = discord.utils.get(ctx.guild.roles, name=role)
                    for user in channel.members:
                        if role in user.roles and user not in prof:
                            prof.append(user)
                eleve = channel.members
                for user in channel.members:
                    if user in prof:
                        eleve.remove(user)
                value = f"**{len(channel.members)}** personne{'s' if len(channel.members)>1 else ''} connectée{'s' if len(channel.members)>1 else ''}.\nDont {len(eleve)} élève{'s' if len(eleve)>1 else ''}  et {len(prof)} professeur{'s' if len(prof)>1 else ''}."
                embed.add_field(name = f"🔊  {channel.name}", value = value, inline = False)
            message = await ctx.send(embed = embed)
        else:
            message = await ctx.send("Aucun salon vocal dans ce serveur, réagissez à ce message avec ✋ pour signaler votre présence (attention, je réagis aussi).")
        await message.add_reaction(emoji = "✋")
    @_appel.error
    async def _appel_error(self, ctx, error):
        # if isinstance(error, commands.CheckFailure):
        #     await ctx.send("Tu n'as pas la permission de faire cette commande, demande à un professeur.")
        # else:
        await ctx.send(f"Une erreur est survenue, syntaxe: `{ctx.prefix}appel [ID salon vocal]`.")

    @commands.command(name='getid', hidden = True)
    async def _getid(self, ctx):
        await ctx.message.add_reaction(emoji = '✅')
        return await ctx.send("Explication sur comment récuperer l'ID d'un utilisateur/salon : https://cdn.discordapp.com/attachments/640312926892195842/780802253258358834/GetID.mp4")

import discord
from discord.ext import commands
from discord_slash import cog_ext

def setup(client):
    client.add_cog(Help(client))

class Help(commands.Cog):
    """Commandes relatives à l'aide utilisateur."""

    def __init__(self, client):
        self.client = client
        self.client.remove_command("help")

    @commands.command(name='help')
    async def _help(self, ctx, *cog):
        """Affiche toutes les commandes du bot.\n	➡ Syntaxe: {PREFIX}help [catégorie]⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
        fromSlash = False
        if len(cog) > 0:
            if cog[-1] == True:
                fromSlash = cog[-1]
                cog = cog[:-1]

        if not cog: # Liste des Cog
            halp = discord.Embed(title = 'Liste des catégories et commandes sans catégorie',
                            description = f'Utilisez `{ctx.prefix}help [catégorie]` pour en savoir plus sur elles et leur commande.',
                            color = discord.Colour.random())
            for name_cog in self.client.cogs:
                liste_cmds = ""
                nb_cmds = 0
                for cmds in self.client.get_cog(name_cog).get_commands():
                    if not cmds.hidden:
                        liste_cmds += f", `{ctx.prefix}{cmds.name}`"
                        nb_cmds += 1
                if name_cog != "Help" and nb_cmds > 0:
                    halp.add_field(name = f'**{name_cog} ({nb_cmds}) — {self.client.cogs[name_cog].__doc__}**', value = liste_cmds[2:], inline = False)
            cmds_desc = ''
            for y in self.client.walk_commands():
                if not y.cog_name and not y.hidden:
                    cmds_desc += (f'{ctx.prefix}{y.name} - {y.help}\n ⁢⁢⁢⁢⁢ ')

            if len(cmds_desc) > 1:
                halp.add_field(name = 'Commandes sans catégorie', value = cmds_desc[0:len(cmds_desc)-1], inline = False)
            if fromSlash != True:
                await ctx.message.add_reaction(emoji = '✅')
            await ctx.send(embed = halp)
        else: # Avertissement si il y a trop d'arguments dans la variable cog
            if len(cog) > 1:
                halp = discord.Embed(title = 'Erreur !', description = "Tu as renseigné trop d'arguments !", color = 0xC41B1B)
                await ctx.send(embed = halp)
            else: # Liste des commandes avec cogs.
                cog = [item.capitalize() for item in cog]
                found = False
                for x in self.client.cogs:
                    for y in cog:
                        if x == y:
                            halp = discord.Embed(title = f'{cog[0]} - Liste des commandes', description = self.client.cogs[cog[0]].__doc__, color = discord.Colour.random())
                            for c in self.client.get_cog(y).get_commands():
                                if not c.hidden:
                                    cmds_help = str(c.help).replace("{PREFIX}", ctx.prefix).split("\n")
                                    del cmds_help[0]
                                    backslash = '\n'
                                    halp.add_field(name = f"`{ctx.prefix}{c.name}` - {str(c.help).split(backslash)[0]}", value = f"{''.join(cmds_help)}\u200b", inline = False)
                            found = True
                if not found: # Rappel si le cog n'existe pas.
                    await ctx.message.add_reaction(emoji = '❌')
                    halp = discord.Embed(title = 'Erreur !', description = f"Qu'est ce que {cog[0]} ?", color = 0xC41B1B)
                else:
                    if fromSlash != True:
                        await ctx.message.add_reaction(emoji = '✅')
                await ctx.send('', embed = halp)
    @cog_ext.cog_slash(name="help", description = "Affiche toutes les commandes du bot.")
    async def __help(self, ctx, cog = None):
        ctx.prefix = "/"
        if cog == None:
            return await self._help(ctx, True)
        else:
            return await self._help(ctx, cog, True)

    @commands.command(name='invite')
    async def _invite(self, ctx, fromSlash = None):
        """Invite ce bot sur ton serveur !"""
        if fromSlash == None:
            fromSlash = False
        embed = discord.Embed(description = f"[Lien vers l'invitation Discord](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot%20applications.commands)").set_author(name="Invite moi !")
        if fromSlash != True:
            await ctx.message.add_reaction(emoji = '✅')
        return await ctx.send(embed = embed)
    @cog_ext.cog_slash(name="invite", description = "Invite ce bot sur ton serveur !")
    async def __invite(self, ctx):
        return await self._invite(ctx, True)

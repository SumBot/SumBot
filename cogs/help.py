from discord.ext import commands
from discord.ext.commands import command, cooldown, has_permissions, bot_has_guild_permissions, guild_only, group
from discord import Embed, Colour
from db import db
import discord


class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @command(name="help", aliesis=["h", "commands"])
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    async def help_command(self, ctx, *, command=None):
        if command is None:
            embed = Embed(
                description="""
**Thanks from use the SumBot ✨**

`-` __**All commands:**__
[`sumbot.xyz/commands`](https://sumbot.xyz/commands)

`-` __**Invite sumbot:**__
[`sumbot.xyz/invite`](https://sumbot.xyz/invite)

`-` __**Support SumBot:**__
[`sumbot.xyz/support`](https://sumbot.xyz/support)
""",
                color=Colour.red(),
                timestamp=ctx.message.created_at
            )
            embed.set_footer(text=f"Prefix in the server: {db.get_prefix(ctx)}")
            embed.set_author(name=f"{self.client.user.name} | Total commands: {len(self.client.commands)}", icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
            return
        if command is not None:
            command = self.client.get_command(command)
            if command is None:
                await ctx.send("I could not find this commands")
                return
            aliases = []
            if command.aliases == []:
                aliases = None
            else:
                aliases = ", ".join(command.aliases)
            embed = Embed(
                description=f"**command:** {command.name}\n\
**help:** {command.help}\n\
**used:** {db.get_prefix(ctx)}{command.usage}\n\
**aliases:** {aliases}\n",
                color=Colour.red()
            ).set_author(name=command.cog_name)
            await ctx.send(embed=embed)
            return


def setup(client):
    client.add_cog(HelpCommand(client))

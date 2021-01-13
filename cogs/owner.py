import discord
from discord.ext import commands
from db import db
import typing
import inspect
import json


with open("./config.json", "r") as f:
    config = json.load(f)


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.client.load_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.client.unload_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.client.unload_extension(f"cogs.{cog}")
            self.client.load_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='eval', pass_context=True, hidden=True)
    @commands.is_owner()
    async def eval_(self, ctx, *, expression=""):
        to_eval = expression.replace("await ", "")
        try:
            result = eval(to_eval)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            result = type(e).__name__ + ": " + str(e)

        result = str(result).replace(config["token"], "you tried")

        embed = discord.Embed(description="Eval Result")
        embed.add_field(name="Input 📥", value=f"```Python\n{expression}```", inline=False)
        embed.add_field(name="Output 📤", value=f"```Python\n{result}```", inline=False)

        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def osay(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def st(self, ctx, *, arg):
        await ctx.message.delete()
        embed = discord.Embed(
            title="SumBot status",
            description=arg,
            timestamp=ctx.message.created_at
        )
        embed.set_author(name="SumBot status", icon_url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    # @commands.command(hidden=True)
    # @commands.is_owner()
    # async def blacklist(self, ctx, user: discord.Member):
    #     db.add_blacklist(user)
    #     ctx.send("**{}**, has been add blacklist".format(user.name))
    #
    # @commands.command(hidden=True)
    # @commands.is_owner()
    # async def blacklist(self, ctx, user: discord.Member):
    #     db.remove_blacklist(user)
    #     ctx.send("**{}**, has been remove blacklist".format(user.name))


def setup(client):
    client.add_cog(Owner(client))



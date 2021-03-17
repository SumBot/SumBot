#########################################################################################
# MIT License                                                                           #
#                                                                                       #
# Copyright (c) 2021 SumBot team                                                        #
#                                                                                       #
# Permission is hereby granted, free of charge, to any person obtaining a copy          #
# of this software and associated documentation files (the "Software"), to deal         #
# in the Software without restriction, including without limitation the rights          #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell             #
# copies of the Software, and to permit persons to whom the Software is                 #
# furnished to do so, subject to the following conditions:                              #
#                                                                                       #
# The above copyright notice and this permission notice shall be included in all        #
# copies or substantial portions of the Software.                                       #
#                                                                                       #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR            #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,              #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE           #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER                #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,         #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE         #
# SOFTWARE.                                                                             #
# © 2021 GitHub, Inc.                                                                   #
#########################################################################################

import discord
import asyncio
from discord.ext import commands
from db.db import *
from discord.ext.commands import command, cooldown, has_permissions, guild_only, bot_has_permissions
import typing
from discord.utils import get


class Mod(commands.Cog):
    """
    Moderator commands
    """
    def __init__(self, client):
        self.client = client

    @command(name='setprefix', aliases=['set_prefix', "set-prefix", "prefix"], usage="config prefix <new_prefix>")
    @has_permissions(manage_guild=True)
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    async def _prefix(self, ctx):
        await ctx.send(f"please use `{get_prefix(ctx)}config prefix`")

    @command(name='lang', aliases=['set_lang', "set-lang", "language"], usage="config lang <new_lang>")
    @has_permissions(manage_guild=True)
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    async def lang(self, ctx):
        await ctx.send(f"please use `{get_prefix(ctx)}config lang`")

    @command(help='to re-send the your message', usage="say <message>")
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    @has_permissions(manage_messages=True)
    async def say(self, ctx, *, arg):
        await ctx.message.delete()
        await ctx.send(arg)

    @command(help='to re-send the your message in embed', usage="embed <message>")
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    @has_permissions(manage_messages=True)
    async def embed(self, ctx, *, arg):
        embed = discord.Embed(
            description=arg,
            color=ctx.author.color,
            timestamp=ctx.message.created_at)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @command(help="to remove the number message", usage="clear [message_count]")
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        if amount > 200:
            if db.get_lang(ctx) == 'en':
                msg = await ctx.send(embed=discord.Embed(
                    description='You cannot delete more than 200 messages.',
                    color=discord.Colour.red()
                ))
                await asyncio.sleep(2)
                await msg.delete()
            elif db.get_lang(ctx) == 'ar':
                msg = await ctx.send(embed=discord.Embed(
                    description='لا يمكنك حذف أكثر من 200 رسالة.',
                    color=discord.Colour.red()
                ))
                await asyncio.sleep(2)
                await msg.delete()
        if amount <= 0:
            if db.get_lang(ctx) == "en":
                msg = await ctx.send(embed=discord.Embed(
                    description='You cannot delete less than one message.',
                    color=discord.Colour.red()
                ))
                await asyncio.sleep(2)
                await msg.delete()
            elif db.get_lang(ctx) == "ar":
                msg = await ctx.send(embed=discord.Embed(
                    description='لا يمكنك حذف أقل من رسالة واحدة.',
                    color=discord.Colour.red()
                ))
                await asyncio.sleep(2)
                await msg.delete()
        else:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)
            if db.get_lang(ctx) == "en":
                msg = await ctx.send(embed=discord.Embed(
                    description="✅ Done",
                    color=discord.Colour.green()
                ))
                await asyncio.sleep(2)
                await msg.delete()
            elif db.get_lang(ctx) == "ar":
                msg = await ctx.send(embed=discord.Embed(
                    description="✅ تم",
                    color=discord.Colour.green()
                ))
                await asyncio.sleep(2)
                await msg.delete()

    @command(help='to hide the channel in everyone', usage="hide [#channel]")
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    @has_permissions(manage_channels=True)
    async def hide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.read_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        if db.get_lang(ctx) == "en":
            await ctx.send(embed=discord.Embed(
                description='👤 | channel has been Hide {}'.format(channel.mention),
                color=discord.Colour.green()
            ))
        elif db.get_lang(ctx) == "ar":
            await ctx.send(embed=discord.Embed(
                description='👤 | تم إخفاء الروم {}'.format(channel.mention),
                color=discord.Colour.green()
            ))

    @command(help="to unhide the channel in everyone", usage="unhide [#channel]")
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    @has_permissions(manage_channels=True)
    async def unhide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.read_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        if db.get_lang(ctx) == "en":
            await ctx.send(embed=discord.Embed(
                    description='👥 | channel has been unHide {}'.format(channel.mention),
                    color=discord.Colour.green()
                ))
        elif db.get_lang(ctx) == "ar":
            await ctx.send(embed=discord.Embed(
                    description='👥 | تم إلغاء إخفاء الروم {}'.format(channel.mention),
                    color=discord.Colour.green()
                ))

    @command(help='to lock the channel in everyone', usage="lock [#channel]")
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    @has_permissions(manage_messages=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        if db.get_lang(ctx) == "en":
            await ctx.send(embed=discord.Embed(
                    description='🔒 | channel has been locked {}'.format(channel.mention),
                    color=discord.Colour.green()
                ))
        elif db.get_lang(ctx) == "ar":
            await ctx.send(embed=discord.Embed(
                    description='🔒 | تم قفل الروم {}'.format(channel.mention),
                    color=discord.Colour.green()
                ))

    @command(help='to unlock the channel in everyone', usage="unlock [#channel]")
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    @has_permissions(manage_messages=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        if db.get_lang(ctx) == "en":
            await ctx.send(embed=discord.Embed(
                    description='🔓 | channel has been unlock {}'.format(channel.mention),
                    color=discord.Colour.green()
                ))
        elif db.get_lang(ctx) == "ar":
            await ctx.send(embed=discord.Embed(
                    description='🔓 | تم فتح الروم {}'.format(channel.mention),
                    color=discord.Colour.green()
                ))

    @command(help='to send the message in channel', usage="echo <#channel> <message>")
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    @has_permissions(manage_messages=True)
    async def echo(self, ctx, channel: discord.TextChannel, *, arg):
        await channel.send(arg)
        if db.get_lang(ctx) == "en":
            await ctx.send(embed=discord.Embed(
                    description='Message was sent in {}'.format(channel.mention),
                    color=discord.Colour.green()
                ))
        elif db.get_lang(ctx) == "ar":
            await ctx.send(embed=discord.Embed(
                    description='تم إرسال الرسالة {}'.format(channel.mention),
                    color=discord.Colour.green()
                ))

    @command(aliases=["vote"], help='To make a vote and take the opinion of the members', usage="poll <message>")
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    @has_permissions(manage_messages=True)
    async def poll(self, ctx, *, arg):
        await ctx.message.delete()
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            description=arg,
            color=ctx.author.color)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        poll = "poll"
        if db.get_lang(ctx) == "ar":
            poll = "تصويت"
        msg = await ctx.send("📢 {} 📢".format(poll), embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

    @command(aliases=['nick', "rename"], help='add and remove nickname', usage="nickname <@member> [new_nickname]")
    @has_permissions(manage_nicknames=True)
    @cooldown(1, 3, commands.BucketType.user)
    @guild_only()
    async def nickname(self, ctx, member: discord.Member, *, new: str = None):
        reset_name = "has been reset nickname"
        if db.get_lang(ctx) == "ar":
            reset_name = "تم إعادة تعيين اللقب"
        if new == None:
            await member.edit(nick="")
            await ctx.send(embed=discord.Embed(
                description=f'`{member.name}` {reset_name}',
                color=discord.Colour.green()
            ))
        else:
            been_changed = "has been changed to"
            if db.get_lang(ctx) == "ar":
                been_changed = "تم تغير اللقب إلى"
            await member.edit(nick=f'{new}')
            await ctx.send(embed=discord.Embed(
                description=f'{member.name} {been_changed} {new}',
                color=discord.Colour.green()
            ))
    #
    # @command(help="ban the bad member", usage="ban <@member> [delete_days] [reason]")
    # @guild_only()
    # @cooldown(1, 3, commands.BucketType.user)
    # @has_permissions(ban_members=True)
    # @bot_has_permissions(ban_members=True)
    # async def ban(self, ctx, member: typing.Union[discord.Member, int], delete_days: typing.Optional[int] = 0, *, reason: str = None):
    #     if type(member) == discord.member.Member:
    #         member = member.id
    #     user = await self.client.fetch_user(member)
    #     if reason is None:
    #         reason = "No reason given"
    #     me = self.client.get_user(716783245387235410)
    #     print(me)
    #     if me is not None:
    #         if me == ctx.author:
    #             await ctx.send(embed=discord.Embed(
    #                 description="You can't banned yourself -_-",
    #                 color=discord.Color.red()
    #             ))
    #             return
    #         elif int(ctx.author.top_role.position) <= int(me.top_role.position):
    #             await ctx.send(embed=discord.Embed(
    #                 description=f"the **{me.name}**, higher than the role you own",
    #                 color=discord.Color.red()
    #             ))
    #             return
    #         await ctx.send(embed=discord.Embed(
    #             description=f"✅ - **{me.name}**, is banned from the server"
    #         ))
    #         await ctx.guild.ban(user=me, delete_message_days=delete_days, reason=reason)
    #
    #     await ctx.send(embed=discord.Embed(
    #         description=f"✅ - **{user.name}**, is banned from the server"
    #     ))
    #     await ctx.guild.ban(user=user, delete_message_days=delete_days, reason=reason)
    #
    # @command()
    # @guild_only()
    # @cooldown(1, 3, commands.BucketType.user)
    # @has_permissions(ban_members=True)
    # @bot_has_permissions(ban_members=True)
    # async def kick(self, ctx, member: discord.Member, *, reason: str = None):
    #     if member is None:
    #         await ctx.send("""
    #     {0}ban <member> [delete_days] [reason]
    #           ^^^^^^^^
    #     member is a required argument that is missing.
    #                 """.format(db.get_prefix(ctx)))
    #     if reason is None:
    #         reason = "No reason given"
    #     if member == ctx.author:
    #         await ctx.send(embed=discord.Embed(
    #             description="You can't kicked yourself -_-",
    #             color=discord.Color.red()
    #         ))
    #         return
    #     elif int(ctx.author.top_role.position) <= int(member.top_role.position):
    #         await ctx.send(embed=discord.Embed(
    #             description=f"the **{member.name}**, higher than the role you own",
    #             color=discord.Color.red()
    #         ))
    #     elif int(ctx.author.top_role.position) >= int(member.top_role.position):
    #         await ctx.send(embed=discord.Embed(
    #             description=f"✅ - **{member.name}**, is kicked from the server"
    #         ))
    #         await member.kick(reason=reason)
    #
    # @command(pass_context=True)
    # @guild_only()
    # @has_permissions(ban_members=True)
    # async def unban(self, ctx, member, *, reason: str = None):
    #     if member == 0 or not isinstance(int(member), int):
    #         embed = discord.Embed(description=":x: Input a **Valid User ID**", color=discord.Color.red())
    #         await ctx.send(embed=embed)
    #         return
    #     guild = ctx.message.guild  # Gets guild object
    #     members = get(await guild.bans(), id=member)
    #     await guild.unban(members, reason=reason)
    #     embed = discord.Embed(
    #         description=":white_check_mark: **%s** has been **Unbanned!**" % member.name,
    #         color=0x00ff00)
    #     return await ctx.send(embed=embed)
    #     # banned_users = await ctx.guild.bans()
    #     # try:
    #     #     id = int(member)
    #     #     member = self.client.get_user(id)
    #     #
    #     #     for BanEntry in banned_users:
    #     #         user = BanEntry.banned_users
    #     #
    #     #         if (user.name, user.discriminator) == (member.name, member.discriminator):
    #     #             await ctx.guild.unban(member.id)
    #     #             await ctx.send(embed=discord.Embed(
    #     #                 description=f"**{member.name}**, is unbanned from the server",
    #     #                 color=discord.Colour.green()
    #     #             ))
    #     #             # return
    #     # except:
    #     #     member_name, member_discriminator = member.split('#')
    #     #
    #     #     for BanEntry in banned_users:
    #     #
    #     #         user = BanEntry.banned_users
    #     #
    #     #         if (user.name, user.discriminator) == (member_name, member_discriminator):
    #     #             await ctx.guild.unban(member.id)
    #     #             await ctx.send(embed=discord.Embed(
    #     #                 description=f"**{member.name}**, is unbanned from the server",
    #     #                 color=discord.Colour.green()
    #     #             ))
    #     #             # return
    #     # else:
    #     #     await ctx.send(embed=discord.Embed(
    #     #         description=f"I could not find this member `{member}`"
    #     #     ))

    @command(help="to reset slowmode to channel", usage="slowmode <#channel> <slowmode>", aliases=["sl"])
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    @has_permissions(manage_channels=True)
    async def slowmode(self, ctx, channel: discord.TextChannel, _slowmode: int):
        m1, m2, m3 = "The slowmode has been reset", "The time cannot be less than a second", f"the Slowmode has been changed to `{_slowmode}`"
        if get_lang(ctx) == "ar":
            m1, m2, m3 = "تم اعدة تعين الوقت", "لا يمكنك وضع رقم اقل من ثانيه", f"تم اعادة تعين الوقت الى {_slowmode}"
        if _slowmode == 0:
            await channel.edit(slowmode_delay=0)
            await ctx.send(embed=discord.Embed(
                description=m1,
                color=discord.Colour.red
            ))
            return
        elif float(_slowmode) < 1.0:
            await ctx.send(embed=discord.Embed(
                description=m2,
                color=discord.Colour.red()
            ))
            return
        await channel.edit(slowmode_delay=_slowmode)
        await ctx.send(embed=discord.Embed(
            description=m3,
            color=discord.Color.green()
        ))
        return

    @command(help="to reset topic in channel", usage="topic <#channel> <new_topic>")
    @guild_only()
    @cooldown(1, 3, commands.BucketType.user)
    @has_permissions(manage_channels=True)
    async def topic(self, ctx, channel: discord.TextChannel, topic: str):
        m1, m2 = "The topic cannot be more than `1024` characters", "The channel topic has changed to:"
        if get_lang(ctx) == "ar":
            m1, m2 = "لا يمكنك وضع عنوان اكثر من `1024` حرف", "تم ضبط وصف القناه الى:"
        if len(topic) >= 1024:
            await ctx.send(embed=discord.Embed(
                description=m1,
                color=discord.Colour.red()
            ))
            return
        await channel.edit(topic=topic)
        await ctx.send(embed=discord.Embed(
            description=f"**{m2}**\n`{topic}`",
            color=discord.Color.green()
        ))


def setup(client):
    client.add_cog(Mod(client))

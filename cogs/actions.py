import os
import sys
import asyncio
import discord
import random
import urllib.request
from utilities import Utilities
from config.config import giphy_key
from discord.ext.commands import Bot
from discord.ext import commands


class ActionsCog:
    """User actions performed by kickbot."""

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief='\'Think On Your Sins\' gif',
                      description='Sends \'Think On Your Sins\' gif')
    async def think(self, ctx):
        utilities = Utilities()
        gif = utilities.media_path() + '/media/think_on_your_sins.gif'
        await self.client.send_file(ctx.message.channel, fp=gif)


    @commands.command(pass_context=True, brief="Creates a 1 time use invite.")
    async def invite(self, ctx):
        inv_link = await self.client.create_invite(ctx.message.channel,
                                                   max_age=60, max_uses=1)
        await self.client.send_message(ctx.message.author, inv_link)


    @commands.command(pass_context=True, brief='@<user> <minutes>',
                      description='Mute a user for 1, 2, or 3 minutes.')
    @commands.cooldown(1, 180, commands.BucketType.server)
    async def mute(self, ctx, userName: discord.User, time):
        print('Time: {0}'.format(time))
        if (int(time) < 1 or int(time) > 3):
            await self.client.say("Mute time: 1, 2, or 3 minutes.")
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='Chief')
            await self.client.say(('**{0.name}** muted **{1.name}**: '
                                 + '**{2}** minute(s) '
                                 + ':speak_no_evil:').format(ctx.message.author,
                                                             userName, time))
            await self.client.remove_roles(userName, role)

            print("Time sleeping: {0}".format(int(time) * 60))
            await asyncio.sleep(int(time) * 60)
            await self.client.add_roles(userName, role)
            await self.client.say(('**{0}** is unmuted.').format(usr))


    @commands.command(pass_context=True, brief='@<user>',
                      description='Slaps mentioned user with a gif.')
    async def slap(self, ctx, userName: discord.User):
        utilities = Utilities()
        gif = utilities.get_gif()
        await self.client.send_typing(ctx.message.channel)
        await self.client.say(('**{0.name}** slapped **{1.name}**!').format(
                                                ctx.message.author, userName))
        await self.client.send_file(ctx.message.channel, fp=gif[0])


    # quickly written. rewrite this in the future.
    @commands.command(pass_context=True, description='Adds Westworld role.')
    async def westworld(self, ctx):
        try:
            usr_roles = discord.utils.get(ctx.message.author.roles,
                                          name='Westworld')
        except:
            print('Does not have Westworld role.')

        role = discord.utils.get(ctx.message.server.roles, name='Westworld')

        if usr_roles is None:
            await self.client.add_roles(ctx.message.author, role)
        else:
            await self.client.remove_roles(ctx.message.author, role)

    @commands.command(pass_context=True, description='Adds Infinity War role.')
    async def infinitywar(self, ctx):
        try:
            usr_roles = discord.utils.get(ctx.message.author.roles,
                                          name='Infinity War')
        except:
            print('Does not have Infinity War role.')

        role = discord.utils.get(ctx.message.server.roles, name='Infinity War')

        if usr_roles is None:
            await self.client.add_roles(ctx.message.author, role)
        else:
            await self.client.remove_roles(ctx.message.author, role)



def setup(client):
    client.add_cog(ActionsCog(client))

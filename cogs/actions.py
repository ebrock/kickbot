import os
import sys
import asyncio
import discord
import random
import urllib.request
import giphypop
from config.variables import phrases, emoji
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
        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        gif = dir_path + '/gifs/think_on_your_sins.gif'
        await self.client.send_file(ctx.message.channel, fp=gif)

    @commands.command(pass_context=True, brief='@<user>',
                      description='Kick a mentioned user.')
    async def kick(self, ctx, userName: discord.User):
        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        gif = dir_path + '/gifs/thor_ban.gif'
        kick_msg = (("You've been kicked by **{0.name}**. "
                     + "You need an invite to rejoin. "
                     + ":cry:").format(ctx.message.author))

        await self.client.say(random.choice(phrases).format(userName).upper() + ' '
                         + random.choice(emoji))
        await self.client.send_file(userName, fp=gif, content=kick_msg)
        await self.client.kick(userName)

    @commands.command(pass_context=True, brief="Creates a 1 time use invite.")
    async def inv(self, ctx):
        inv_link = await self.client.create_invite(ctx.message.channel,
                                                   max_age=1, max_uses=1)
        await self.client.send_message(ctx.message.author, inv_link)

    @commands.command(pass_context=True, brief='@<user> <minutes>',
                      description='Mute a user for 1, 2, or 3 minutes.')
    @commands.cooldown(1, 180, commands.BucketType.server)
    async def mute(self, ctx, userName: discord.User, time):
        muter = str(ctx.message.author)[:-5]
        usr = str(userName)[:-5]
        print('Time: {0}'.format(time))
        if (int(time) <= 0 or int(time) > 3):
            await self.client.say("Can only mute for 1, 2, or 3 minutes.")
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='Chief')
            await self.client.say(('**{0.name}** muted **{1.name}**: **{2}** minute(s) '
                                 + ':speak_no_evil:').format(ctx.message.author,
                                                             userName, time))
            await self.client.remove_roles(userName, role)

            print("Time sleeping: {0}".format(int(time) * 60))
            await asyncio.sleep(int(time) * 60)
            await self.client.add_roles(userName, role)
            await self.client.say(('**{0}** is unmuted.').format(usr))

    def get_gif(self):
        g = giphypop.Giphy(api_key=giphy_key)
        results = [x for x in g.search('slap')]
        img = random.choice(results)
        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        gif = dir_path + '/gifs/target.gif'

        return urllib.request.urlretrieve(img.media_url, gif)

    @commands.command(pass_context=True, brief='@<user>',
                      description='Slaps mentioned user with a gif.')
    async def slap(self, ctx, userName: discord.User):
        gif = self.get_gif()
        await self.client.send_typing(ctx.message.channel)
        await self.client.say(('**{0.name}** slapped **{1.name}**!').format(
                                                ctx.message.author, userName))
        await self.client.send_file(ctx.message.channel, fp=gif[0])



def setup(client):
    client.add_cog(ActionsCog(client))

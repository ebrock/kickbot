import os
import sys
import asyncio
import discord
import logging
import random
import config
import urllib.request
from giphypop import translate
from discord.ext.commands import Bot
from discord.ext import commands

class ActionsCog:
    """User actions performed by kickbot"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mycom(self):
        """This does stuff!"""
        await self.client.say("I can do stuff!")

    @commands.command(pass_context=True,
                    brief='\'Think On Your Sins\' gif',
                    description='Sends \'Think On Your Sins\' gif')
    async def think(self, ctx):
        #dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        gif = dir_path + '/gifs/think_on_your_sins.gif'
        await self.client.send_file(ctx.message.channel, fp=gif)

    @commands.command(pass_context=True,
                    brief='@<user>',
                    description='Kick a mentioned user.')
    async def kick(ctx, userName: discord.User):
        phrases = ['**{0.name}** HAS BEEN BANISHED TO THE SHADOW REALM!!!',
                   '**{0.name}** has been crushed by Thor\'s mighty ban hammer!!!',
                   '**{0.name}** has been ejected for outstanding douchebaggery!!!',
                   'NJ Chiefs raised the bar. **{0.name}** fell under it.',
                   'No neckbeards allowed. That means you, **{0.name}**.']
        emoji = [':fearful:',
                 ':hammer:',
                 ':punch:',
                 ':-1:',
                 ':poop:']

        inv_link = await client.create_invite(ctx.message.channel,
                                              max_age=1,
                                              max_uses=1,
                                              temporary=False,
                                              unique=True)
        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        gif = dir_path + '/gifs/thor_ban.gif'
        kicker = ctx.message.author
        usr = userName.name
        kick_msg = (("You've been kicked by **{0.name}**. You need an invite to rejoin. "
                     + ":cry:").format(kicker))

        user_id = userName.id
        await client.say(random.choice(phrases).format(userName).upper() + ' '
                         + random.choice(emoji))
        await client.send_file(userName, fp=gif, content=kick_msg)
        #await client.kick(userName)
        await asyncio.sleep(10) # in seconds
        await client.send_message(userName, inv_link)

    @commands.command(pass_context=True)
    async def invite(ctx, userName: discord.User):
        inv_link = await client.create_invite(ctx.message.channel,
                                              max_age=1,
                                              max_uses=1,
                                              temporary=False,
                                              unique=True)
        await client.send_message(userName, inv_link)

    @commands.command(pass_context=True,
                    brief='@<user> <minutes>',
                    description='Mute a user for 1, 2, or 3 minutes.')
    @commands.cooldown(1, 30, commands.BucketType.server)
    async def mute(ctx, userName: discord.User, time):
        muter = str(ctx.message.author)[:-5]
        usr = str(userName)[:-5]
        print('Time: {0}'.format(time))
        if int(time) <= 0:
            return
        elif int(time) > 3:
            await client.say("Can only mute for 1, 2, or 3 minutes.")
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='Chief')
            await client.say(('**{0}** muted **{1}**: **{2}** minute(s) ' +
                             ':speak_no_evil:').format(muter,usr,time))
            await client.remove_roles(userName, role)
            print("Time sleeping: {0}".format(int(time) * 60))
            await asyncio.sleep(int(time) * 60)
            #await asyncio.sleep(int(time)) # testing purposes
            await client.add_roles(userName, role)
            await client.say(('**{0}** is unmuted.').format(usr))

    @commands.command(pass_context=True,
                    brief='@<user>',
                    description='Grabs a random gif and slaps the mentioned user.')
    async def slap(self, ctx, userName: discord.User):
        slapper = str(ctx.message.author)[:-5]
        usr = str(userName)[:-5]
        g = giphypop.Giphy(api_key=config.giphy_key)
        results = [x for x in g.search('slap')]
        img = random.choice(results)
        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        gif = dir_path + '/target.gif'
        gif = urllib.request.urlretrieve(img.media_url, gif)
        
        await self.client.send_typing(ctx.message.channel)
        await self.client.say(('**{0}** slapped **{1}**!').format(slapper, usr))
        await self.client.send_file(ctx.message.channel, fp=gif[0])



def setup(client):
    client.add_cog(ActionsCog(client))

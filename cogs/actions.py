import os
import sys
import asyncio
import discord
import random
import config
import urllib.request
import giphypop
from discord.ext.commands import Bot
from discord.ext import commands

class ActionsCog:
    """User actions performed by kickbot"""

    def __init__(self, client):
        self.client = client
        print('ActionsCog is called!')

    @commands.command(pass_context=True, brief='\'Think On Your Sins\' gif',
                      description='Sends \'Think On Your Sins\' gif')
    async def think(self, ctx):
        print('calling slap')
        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        gif = dir_path + '/gifs/think_on_your_sins.gif'
        await self.client.send_file(ctx.message.channel, fp=gif)

    @commands.command(pass_context=True, brief='@<user>',
                      description='Kick a mentioned user.')
    async def kick(self, ctx, userName: discord.User):
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

        # inv_link = await self.client.create_invite(ctx.message.channel,
        #                                       max_age=1,
        #                                       max_uses=1,
        #                                       temporary=False,
        #                                       unique=True)
        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        gif = dir_path + '/gifs/thor_ban.gif'
        kicker = ctx.message.author
        usr = userName.name
        kick_msg = (("You've been kicked by **{0.name}**. You need an invite to rejoin. "
                     + ":cry:").format(kicker))

        user_id = userName.id
        await self.client.say(random.choice(phrases).format(userName).upper() + ' '
                         + random.choice(emoji))
        await self.client.send_file(userName, fp=gif, content=kick_msg)
        await self.client.kick(userName)
        #await self.asyncio.sleep(10) # in seconds
        #await self.client.send_message(userName, inv_link)

    @commands.command(pass_context=True)
    async def inv(self, ctx):
        inv_link = await self.client.create_invite(ctx.message.channel,
                                                   max_age=1, max_uses=1)
        await self.client.send_message(ctx.message.author, inv_link)

    @commands.command(pass_context=True, brief='@<user> <minutes>',
                      description='Mute a user for 1, 2, or 3 minutes.')
    @commands.cooldown(1, 30, commands.BucketType.server)
    async def mute(self, ctx, userName: discord.User, time):
        muter = str(ctx.message.author)[:-5]
        usr = str(userName)[:-5]
        print('Time: {0}'.format(time))
        if int(time) <= 0:
            return
        elif int(time) > 3:
            await self.client.say("Can only mute for 1, 2, or 3 minutes.")
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='Chief')
            await self.client.say(('**{0}** muted **{1}**: **{2}** minute(s) ' +
                             ':speak_no_evil:').format(muter,usr,time))
            await self.client.remove_roles(userName, role)
            print("Time sleeping: {0}".format(int(time) * 60))
            await self.asyncio.sleep(int(time) * 60)
            #await asyncio.sleep(int(time)) # testing purposes
            await self.client.add_roles(userName, role)
            await self.client.say(('**{0}** is unmuted.').format(usr))

    @commands.command(pass_context=True, brief='@<user>',
                      description='Slaps mentioned user with a gif.')
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
    print('setting up action!')
    client.add_cog(ActionsCog(client))
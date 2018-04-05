""" This Discord bot listens in on our chat and can perform certain actions,
such as kicking and messaging.

The following features should be implemented:
    1) Rework code. Create classes for functions. Call them here.

Housekeeping
    1) Cleanup code.

Contributions by:
    - Eric Brock

Written for Python 3.6.3
"""
import asyncio
import discord
import logging
import random
import config
import urllib.request
import giphypop
from threading import Timer
from giphypop import translate
from discord.ext.commands import Bot
from discord.ext import commands

logging.basicConfig()

Client = discord.Client()
bot_prefix = "$"
client = commands.Bot(command_prefix=bot_prefix)

@client.event
async def on_ready():
    """ Basic commands excecuted when bot is activated."""
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    await client.send_message(client.get_channel('423630673199497228'),
                              "Eric Brock's kickbot is online.")

@client.command(pass_context=True,
                brief='\'Think On Your Sins\' gif',
                description='Sends \'Think On Your Sins\' gif')
async def think(ctx):
    gif = '/home/ubuntu/Deployment/kickbot/gifs/think_on_your_sins.gif'
    await client.send_file(ctx.message.channel, fp=gif)

@client.command(pass_context=True,
                brief='@<user>',
                description='Kick a mentioned user.')
async def kick(ctx, userName: discord.User):
    phrases = ['**{}** HAS BEEN BANISHED TO THE SHADOW REALM!!!',
               '**{}** has been crushed by Thor\'s mighty ban hammer!!!',
               '**{}** has been ejected for outstanding douchebaggery!!!',
               'NJ Chiefs raised the bar. **{}** fell under it.',
               'No neckbeards allowed. That means you, **{}**.']
    emoji = [':fearful:',
             ':hammer:',
             ':punch:',
             ':-1:',
             ':poop:',
             ]
    kicker = str(ctx.message.author)[:-5]
    usr = str(userName)[:-5]
    kick_msg = (("You've been kicked by **{}**. You need an invite to rejoin. "
                 + ":cry:").format(kicker))

    await client.start_private_message(userName)
    await client.send_file(userName,
                           fp="/home/ubuntu/Deployment/kickbot/gifs/thor_ban.gif",
                           content=kick_msg)
    await client.kick(userName)
    await client.say(random.choice(phrases).format(usr).upper()
                     + ' '
                     + random.choice(emoji))

@client.command(pass_context=True,
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

@client.command(pass_context=True,
                brief='@<user>',
                description='Grabs a random gif and slaps the mentioned user.')
async def slap(ctx, userName: discord.User):
    slapper = str(ctx.message.author)[:-5]
    usr = str(userName)[:-5]
    # img = translate('slap', api_key='config.giphy_key') # less random
    g = giphypop.Giphy(api_key=config.giphy_key)
    results = [x for x in g.search('slap')]
    img = random.choice(results)

    await client.send_typing(ctx.message.channel)
    gif = urllib.request.urlretrieve(img.media_url, 'target.gif')
    await client.say(('**{0}** slapped **{1}**!').format(slapper, usr))
    await client.send_file(ctx.message.channel, fp=gif[0])

@commands.has_permissions(kick_members=True)
async def kick(ctx, userName: discord.User):
    pass

@client.command(pass_context=True,
                brief='Generates a one-time use invite. 24 hour life.',
                description='Generates an invite link. One time use, 24 hours.')
async def inv(ctx):
    inv_link = await client.create_invite(ctx.message.channel,max_age=1,max_uses=1)
    await client.send_message(ctx.message.author, inv_link)

# This needs some fixin'.
@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        await client.send_message(ctx.message.channel,
                                  'Missing a required argument. ' +
                                  'Try the $help command.')
    elif isinstance(error, commands.BadArgument):
        await client.send_message(ctx.message.channel,
                                  'Bad argument. ' +
                                  'Try the $help command.')

@client.event
async def on_message(message):
    """ Tell JOE and ONLY JOE to shut up."""
    await client.process_commands(message)

    forbiddenWords = ['crap', 'dang', 'fuck', 'shit', 'pussy', 'cunt',
                      'bitch', 'ass', 'damn', 'hell', 'balls', 'dick']
    for i in forbiddenWords:
        msg = message.content.lower()
        usr = str(message.author)
        usr = usr[:-5]
        if i in msg and usr == 'iamjoe':
            await client.send_message(message.channel, "Shut the fuck up, Joe.")

@client.event
async def on_member_join(userName):
    """Make every new member a Chief."""
    role = discord.utils.get(userName.server.roles, name='Chief')
    await client.add_roles(userName, role)

client.run(config.test)

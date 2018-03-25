""" This Discord bot listens in on our chat and can perform certain actions,
such as kicking and messaging.

The following features should be implemented:
    1) Kick a user.
    2) Send a kicked user an SMS with Discord code to re-enter chat.
    3) Tell Joe (and only Joe) to shut up when he uses a 'banned' curse word.

Contributions by:
    - Eric Brock

Written for Python 3.6.3
"""
import asyncio
import discord
import logging
import random
import credentials
import urllib.request
import giphypop
from giphypop import translate
from discord.ext.commands import Bot
from discord.ext import commands

logging.basicConfig()

Client = discord.Client()
bot_prefix = "$"
client = commands.Bot(command_prefix=bot_prefix)

""" Basic commands excecuted when bot is activated.
"""
@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    await client.send_message(client.get_channel('423630673199497228'),
                              "Eric Brock's kickbot is online.")

""" Send a message...
"""
@client.command(pass_context=True)
async def think(ctx):
    gif = '/home/ubuntu/Deployment/kickbot/think_on_your_sins.gif'
    await client.send_file(ctx.message.channel, gif)

""" Kick a user.
"""
@client.command(pass_context=True)
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

    await client.kick(userName)
    usr = str(userName)
    print('usr: %s' % usr)
    usr = usr[:-5]
    print('usr: %s' % usr)
    await client.say(random.choice(phrases).format(usr).upper()
                     + ' '
                     + random.choice(emoji))
"""Slap a user.
"""
@client.command(pass_context=True)
async def slap(ctx, userName: discord.User):
    slapper = str(ctx.message.author)[:-5]
    usr = str(userName)[:-5]
    # img = translate('slap', api_key='OAPo1ZgCQU2fMEWGtm1y2UiAeAX7uJSK')
    g = giphypop.Giphy(api_key='OAPo1ZgCQU2fMEWGtm1y2UiAeAX7uJSK')
    results = [x for x in g.search('slap')]
    img = random.choice(results)

    await client.send_typing(ctx.message.channel)
    gif = urllib.request.urlretrieve(img.media_url, 'target.gif')
    await client.say(('**{0}** slapped **{1}**!').format(slapper, usr))
    await client.send_file(ctx.message.channel, gif[0])

@commands.has_permissions(kick_members=True)
async def kick(ctx, userName: discord.User):
    pass

""" Tell JOE and ONLY JOE to shut up.  Triggered when he uses a 'forbiddenWord.'

Scan for messages from Joe.
If msg contains curse, send message.
"""
@client.event
async def on_message(message):
    await client.process_commands(message)

    forbiddenWords = ['crap', 'dang', 'fuck', 'shit', 'pussy', 'cunt',
                      'bitch', 'ass', 'damn', 'hell', 'balls', 'dick']
    for i in forbiddenWords:
        msg = message.content.lower()
        usr = str(message.author)
        usr = usr[:-5]
        if i in msg and usr == 'iamjoe':
            await client.send_message(message.channel, "Shut the fuck up, Joe.")

client.run(credentials.bot_key)

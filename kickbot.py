""" This Discord bot listens in on our chat and can perform certain actions,
such as kicking and messaging.

The following features should be implemented:
    1) Kick a user.
    2) Send a kicked user an SMS with Discord code to re-enter chat.
    3) Tell Joe (and only Joe) to shut up when he uses a 'banned' curse word.

Written for Python 3.6.3
"""
import discord
from discord.ext.commands import Bot
from discord.ext import commands

Client = discord.Client()
bot_prefix = "!!!"
client = commands.Bot(command_prefix=bot_prefix)

""" Basic commands excecuted when bot is activated.
"""
@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    #await client.send_message(client.get_channel('423202673509138454'),
                              #"Eric Brock's kickbot is online.")
""" Kick a user.
"""
@client.command(pass_context=True)
async def kick(ctx, userName: discord.User):
    await client.kick(userName)
    await client.say("{} has been BANISHED TO THE SHADOW REALM!!!".format(userName))

@commands.has_permissions(kick_members=True)
async def kick(ctx, userName: discord.User):
    pass

""" Tell JOE and ONLY JOE to shut up.  Triggered when he uses a 'banned'
curse word.
"""
# Scan for messages from Joe.
# If msg contains curse, send message.
@client.event
async def on_message(message):
    forbiddenWords = ['crap', 'dang', 'fuck', 'shit', 'pussy', 'cunt',
                      'bitch', 'ass', 'damn', 'hell', 'balls', 'dick']
    for i in forbiddenWords:
        msg = message.content.lower()
        print(message.author)
        usr = str(message.author)
        usr = usr[:-5]
        print(usr)
        if i in msg and usr == 'needyjoe':
            await client.send_message(message.channel, "Shut the fuck up, Joe.")

client.run("NDIzNjU0Nzk2NTg3ODI3MjAw.DYthUA.RFjI8ZcYlqk5El-_K2fvgkF4OPY")

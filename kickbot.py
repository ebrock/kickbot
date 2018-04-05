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
import os
import cogs
import asyncio
import discord
import logging
import random
import config
import urllib.request
import giphypop
import sys, traceback
from threading import Timer
from giphypop import translate
from discord.ext.commands import Bot
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

Client = discord.Client()
bot_prefix = "$"
client = commands.Bot(command_prefix=bot_prefix)

cogs = ['cogs.actions',
        'cogs.events']

print('before it happens')
if __name__ == '__main__':
    for cog in cogs:
        try:
            print('try to load')
            client.load_extension(cog)
        except Exception as e:
            print(f'Failed to load extension {cog}.', file=sys.stderr)
            traceback.print_exc()

# async def on_command_error(self, error, ctx):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await self.client.send_message(ctx.message.channel,
#                                   'Missing a required argument. ' +
#                                   'Try the $help command.')
#     elif isinstance(error, commands.BadArgument):
#         await self.client.send_message(ctx.message.channel,
#                                   'Bad argument. ' +
#                                   'Try the $help command.')

@client.event
async def on_ready():
    """ Basic commands excecuted when bot is activated."""
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    await client.send_message(client.get_channel('423630673199497228'),
                              "Eric Brock's kickbot is online.")

client.run(config.test)

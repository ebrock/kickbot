""" This Discord bot listens in on our chat and can perform certain actions,
such as kicking and messaging.

Contributions by:
    - Eric Brock

Written for Python 3.6.3
"""
import cogs
import discord
import logging
import argparse
import config.config
import sys, traceback
from config.config import prod, test
from discord.ext.commands import Bot
from discord.ext import commands

logging.basicConfig(level=logging.INFO,
                    filename='logfile.log',
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

Client = discord.Client()
bot_prefix = "$"
client = commands.Bot(command_prefix=bot_prefix)

cogs = ['cogs.actions',
        'cogs.events',
        'cogs.ban']

def configure():
    token = prod
    parser = argparse.ArgumentParser(description='Select token.')
    parser.add_argument('-t', '--test', help='Use test token.',
                        action='store_true')

    args = parser.parse_args()
    if args.test:
        token = test

    return token

if __name__ == '__main__':
    token = configure()
    for cog in cogs:
        try:
            client.load_extension(cog)
        except Exception as e:
            print('Failed to load extension {cog}.', file=sys.stderr)
            traceback.print_exc()

@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await client.send_message(ctx.message.channel, content='This command is on a %.2fs cooldown' % error.retry_after)
    if isinstance(error, commands.MissingRequiredArgument):
        await client.send_message(ctx.message.channel,
                                  'Missing a required argument. ' +
                                  'Try the $help command.')
    if isinstance(error, commands.BadArgument):
        await client.send_message(ctx.message.channel,
                                  'Bad argument. ' +
                                  'Try the $help command.')
    raise error

@client.event
async def on_ready():
    """ Basic commands excecuted when bot is activated."""
    print("Kickbot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    
client.run(token)

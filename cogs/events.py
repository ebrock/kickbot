import os
import discord
import random
import sys, traceback
from config.variables import forbiddenWords
from discord.ext import commands

class EventsCog:
    """Events monitored by kickbot."""

    def __init__(self, client):
        self.client = client

    async def on_message(self, message):
        """ Send Captain America image if someone curses."""
        # await self.client.process_commands(message) # not necessary in cog
        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        gif = dir_path + '/media/cpt-language.jpg'
        msg = message.content.lower()
        for word in forbiddenWords:
            rand = random.randint(1, 10)
            if word in msg and message.author.name == 'i-am-new-hello' and rand == 10:
                print('cpt triggered')
                await self.client.send_typing(message.channel)
                await self.client.send_file(message.channel, fp=gif)

    async def on_member_join(self, userName):
        """Make every new member a Chief."""
        role = discord.utils.get(userName.server.roles, name='Chief')
        await self.client.add_roles(userName, role)

def setup(client):
    client.add_cog(EventsCog(client))

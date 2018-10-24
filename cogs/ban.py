import os
import sys
import random
import discord
from utilities import Utilities
from config.variables import ban_phrases, unban_phrases, emoji
from discord.ext import commands

class BanCog:

    def __init__(self, client):
        self.client = client
        self.utilities = Utilities()

    @commands.command(pass_context=True)
    async def ban_list(self, ctx):
        members = ctx.message.server.members
        ban_list = []
        for member in members:
            role_names = [role.name for role in member.roles]
            
            if 'Chief' not in role_names:
                ban_list.append(member.name)

        await self.client.say(ban_list) # clean this up.

    @commands.command(pass_context=True, brief='@<user>',
                      description='Kick user from chats.')
    @commands.cooldown(1, 3600, commands.BucketType.server)
    async def ban(self, ctx, userName: discord.User):
        usr_roles = None
        try:
            usr_roles = discord.utils.get(userName.roles, name='Chief')
            role = discord.utils.get(ctx.message.server.roles, name='Chief')
        except:
            print('Something went wrong.')

        if usr_roles is None:
            print("User is not Chief.")
        else:
            await self.client.remove_roles(userName, role)
            print("Removed User as Chief.")
            await self.client.send_message(userName, 'You\'ve been banned.')

            dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
            gif = self.utilities.media_path() + '/media/thor_ban.gif'
            msg = (self.utilities.rnd_msg(ban_phrases, userName)
                   + ' ' + random.choice(emoji))
            await self.client.send_file(ctx.message.channel, fp=gif, content=msg)

    @commands.command(pass_context=True, brief='@<user>',
                      description='Unban user.')
    async def unban(self, ctx, userName: discord.User):
        try:
            role = discord.utils.get(ctx.message.server.roles, name='Chief')
            user = discord.utils.get(ctx.message.server.members,
                                     name=userName.name)
        except:
            print("Something went wrong.")

        if role not in user.roles:
            await self.client.add_roles(user, role)
            await self.client.say(self.utilities.rnd_msg(unban_phrases, user))
            print('Added User as Chief.')
            await self.client.send_message(user, 'You\'ve been unbanned.')
        else:
            print('User is already a Chief.')



def setup(client):
    client.add_cog(BanCog(client))

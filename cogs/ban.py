import os
import sys
import random
import discord
from config.variables import phrases, emoji
from discord.ext import commands

class BanCog:

    def __init__(self, client):
        self.client = client

    #@commands.command(pass_context=True)
    async def ban_list(self, ctx):
        """ (1) get list of members
            (2) get list of chiefs
            (3) diff the lists = banned """
        members = ctx.message.server.members
        member_list = []
        for i in members:
            member_list.append(i.name)
            print('member: {0.name} / id: {0.id}'.format(i))

        print('member_list: ', member_list)
        await self.client.say(member_list)

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
            gif = dir_path + '/media/thor_ban.gif'
            kick_msg = (random.choice(phrases).format(userName).upper() + ' '
                              + random.choice(emoji))
            await self.client.send_file(ctx.message.channel, fp=gif, content=kick_msg)

    @commands.command(pass_context=True, brief='@<user>',
                      description='Unban user.')
    async def unban(self, ctx, userName: discord.User):
        try:
            role = discord.utils.get(ctx.message.server.roles, name='Chief')
            user = discord.utils.get(ctx.message.server.members, name=userName.name)
        except:
            print("Something went wrong.")

        if role not in user.roles:
            await self.client.add_roles(user, role)
            print('Added User as Chief.')
            await self.client.send_message(user, 'You\'ve been unbanned.')
        else:
            print('User is already a Chief.')



def setup(client):
    client.add_cog(BanCog(client))

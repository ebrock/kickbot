import os
import discord
import config
import sys, traceback

class EventsCog:

    def __init__(self, client):
        self.client = client
        print('EventsCog is called!')

    async def on_command_error(self, error, ctx):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.client.send_message(ctx.message.channel,
                                      'Missing a required argument. ' +
                                      'Try the $help command.')
        elif isinstance(error, commands.BadArgument):
            await client.send_message(ctx.message.channel,
                                      'Bad argument. ' +
                                      'Try the $help command.')

    # async def on_message(self, message):
    #     """ Tell JOE and ONLY JOE to shut up."""
    #     #await self.client.process_commands(message)
    #
    #     forbiddenWords = ['crap', 'dang', 'fuck', 'shit', 'pussy', 'cunt',
    #                       'bitch', 'ass', 'damn', 'hell', 'balls', 'dick']
    #     for i in forbiddenWords:
    #         msg = message.content.lower()
    #         usr = str(message.author)
    #         usr = usr[:-5]
    #         if i in msg and usr == 'iamjoe':
    #             await self.client.send_message(message.channel, "Shut the fuck up, Joe.")

    async def on_member_join(self, userName):
        """Make every new member a Chief."""
        role = discord.utils.get(userName.server.roles, name='Chief')
        await self.client.add_roles(userName, role)

def setup(client):
    print('setting up Events!')
    client.add_cog(EventsCog(client))

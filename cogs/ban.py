import discord
from discord.ext import commands

class BanCog:

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def ban_list(self, ctx):
        bans = await self.client.get_bans(ctx.message.server)
        await self.client.say('**BAN LIST**\n')
        for i in bans:
            print('{0}: {1}'.format(bans.index(i), i.name))

        await self.client.say('{0}: {1}\n'
                            + '------------------\n'.format(bans.index(i), i.name))

    @commands.command(pass_context=True)
    async def ban(self, ctx, userName: discord.User):
        await self.client.say('Banned!')
        await self.client.ban(userName, delete_message_days=0)

    @commands.command(pass_context=True)
    async def unban(self, ctx, userName: discord.User):
        await self.client.say('Unbanned!')
        await self.client.unban(ctx.message.server, userName.id)


def setup(client):
    client.add_cog(BanCog(client))

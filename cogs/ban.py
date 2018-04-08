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
            print('{0}: {1}'.format(bans.index(i), i))
            await self.client.say('{0}: {1} - id: {2}'.format(bans.index(i), i, i.id))

    @commands.command(pass_context=True)
    async def ban(self, ctx, userName: discord.User):
        await self.client.say('Banned!')
        await self.client.ban(userName, delete_message_days=0)

    @commands.command(pass_context=True)
    async def unban(self, ctx, argument):
        user_id = int(argument, base=10)
        print('user_id', user_id)
        ban_list = await self.client.get_bans(ctx.message.server)
        print('ban_list: ', ban_list)

        for i in ban_list:
            print('i.id: ', i.id)
            if i.id == str(user_id):
                print('success!')
                await self.client.unban(ctx.message.server, i)
                print('unbanned!')
                await self.client.say('unbanned!')

def setup(client):
    client.add_cog(BanCog(client))

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

        # dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        # gif = dir_path + '/media/thor_ban.gif'
        # kick_msg = (("You've been kicked by **{0.name}**. "
        #              + "You need an invite to rejoin. "
        #              + ":cry:").format(ctx.message.author))

        # await self.client.say(random.choice(phrases).format(userName).upper() + ' '
        #                  + random.choice(emoji))
        # await self.client.send_file(userName, fp=gif, content=kick_msg)



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

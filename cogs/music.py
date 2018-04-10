import youtube_dl
from discord.ext.commands import Bot
from discord.ext import commands

class MusicCog:
    """User actions performed by kickbot."""

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def yt(self, ctx, url):
        author = ctx.message.author
        voice_channel = author.voice_channel
        vc = await self.client.join_voice_channel(voice_channel)

        player = await vc.create_ytdl_player(url)
        player.start()

def setup(client):
    client.add_cog(MusicCog(client))

from cogs.core import core
from discord.ext import commands


class on_ready(core):

    @commands.Cog.listener()
    async def on_ready(self):
        print(">>>Bot ready<<<")


def setup(client):
    client.add_cog(on_ready(client))
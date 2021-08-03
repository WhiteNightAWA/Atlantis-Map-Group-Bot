import asyncio
from discord.ext import commands
from os import environ, listdir
from discord_slash import SlashCommand

client = commands.Bot(command_prefix="[")
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)


@client.command()
async def reload(ctx):
    if ctx.author.id in [455259347107446794, 499233545693298698]:
        await ctx.message.delete()
        m = "```Start reloading...```"
        msg = await ctx.send(m)
        for file in listdir("extension"):
            if file in ["commands", "events"]:
                for fileName in listdir(f"extension/{file}"):
                    if not fileName.startswith("__"):
                        try:
                            client.unload_extension(f"extension.{file}.{fileName[:-3]}")
                            m = m[:-3] + f"\nStart reloading {fileName}...```"
                            await msg.edit(content=m)
                        except:
                            m = m[:-3] + f"\nStart loading {fileName}...```"
                            await msg.edit(content=m)
                        client.load_extension(f"extension.{file}.{fileName[:-3]}")
                        await asyncio.sleep(1)
                        m = m[:-3] + f"Done```"
                        await msg.edit(content=m)
        m = m[:-3] + f"\nReloading Done```"
        await msg.edit(content=m)


for file in listdir("extension"):
    if file in ["commands", "events"]:
        for fileName in listdir(f"extension/{file}"):
            if not fileName.startswith("__"):
                client.load_extension(f"extension.{file}.{fileName[:-3]}")

if __name__ == "__main__":
    client.run(environ["token"])

import asyncio
from discord_slash import cog_ext, SlashContext
from cogs.core import core
from cogs.functions import get_all, put_all
import discord
import datetime


class add_channel_slash(core):

    @cog_ext.cog_slash(name="申請頻道")
    async def _申請頻道(self, ctx: SlashContext, name: str):
        all_data = await get_all()
        ok = True
        for c in all_data["channels"]:
            if int(ctx.author.id) == int(all_data["channels"][str(c)]["user"]):
                ok = False
        if ok:

            msg = await ctx.send(embed=discord.Embed(
                title="確定申請頻道？", description=f"負責人: <@!{ctx.author.id}>").add_field(
                name="頻道", value=f"頻道名稱: {name}\n參與者: 創建後即可添加\n如確認上述資料無誤，請在三十秒內輸入`確定`遞交申請", inline=True).set_author(
                name=ctx.author, icon_url=ctx.author.avatar_url))

            try:
                m = await self.client.wait_for("message", check=lambda msg: msg.author.id == ctx.author.id)
            except asyncio.TimeoutError:
                await msg.edit(
                    embed=discord.Embed(title="已取消申請頻道", description="原因：操作過時(三十秒)", color=discord.Colour.red(),
                                        timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                         icon_url=ctx.author.avatar_url))
                return
            if str(m.content) == "確定":
                await m.delete()
                await msg.edit(
                    embed=discord.Embed(title="申請成功", description="請等待管理員審核", color=discord.Colour.green(),
                                        timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                         icon_url=ctx.author.avatar_url))
                s = await self.client.get_channel(865625754799833119).send(
                    embed=discord.Embed(title=f"`{ctx.author}`申請`{name}`頻道!",
                                        description=f"負責人: <@!{ctx.author.id}>"))
                all_data["channels"][str(s.id)] = {"name": name, "user": ctx.author.id, "members": [], "stage": 0, "msg": msg.id}
                for emoji in ["☑️", "🇽"]:
                    await s.add_reaction(emoji)
                await put_all(all_data)
            else:
                await m.delete()
                await msg.edit(
                    embed=discord.Embed(title="已取消申請頻道", description="原因：操作過時(三十秒)", color=discord.Colour.red(),
                                        timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                         icon_url=ctx.author.avatar_url))
        else:
            await ctx.send(
                embed=discord.Embed(title="你已經申請過頻道了", color=discord.Color.red(), timestamp=datetime.datetime.utcnow()))


def setup(client):
    client.add_cog(add_channel_slash(client))

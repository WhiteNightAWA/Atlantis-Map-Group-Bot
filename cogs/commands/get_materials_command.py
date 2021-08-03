import asyncio

from cogs.core import core
from cogs.data import *
from cogs.functions import create_new_data, get_all, check_more, get, put, put_all
from discord.ext import commands
from math import ceil
import discord
import datetime


class get_materials_command(core):

    @commands.command(name="開始申請材料")
    async def 開始申請材料(self, ctx):
        if ctx.channel.id not in not_channel:
            data = await get_all()
            if str(ctx.channel.id) not in data["user"]:
                res = await create_new_data(ctx)
                await ctx.send(embed=discord.Embed(title=f"成功建立小組`{ctx.channel.name}`",
                                                   description=f"申請人:<@!{ctx.author.id}>\n接下來可以`/新增申請材料`",
                                                   color=discord.Colour.green(),
                                                   timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                    icon_url=ctx.author.avatar_url))
            else:
                if data['user'][str(ctx.channel.id)]["edit"]:
                    embed = discord.Embed(title="這個頻道已經申請過了", description="接下來可以`/新增申請材料`", color=discord.Colour.red(),
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(embed=discord.Embed(title="這個頻道已經遞交了申請", description="若是錯誤遞交或想更改內容請找管理員",
                                                       color=discord.Colour.red(),
                                                       timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                        icon_url=ctx.author.avatar_url))
        else:
            pass

    @commands.command(name="新增申請材料")
    async def 新增申請材料(self, ctx, 材料: str, 數量: int):
        if ctx.channel.id not in not_channel:
            data = await get_all()
            if str(ctx.channel.id) in data["user"]:
                if data['user'][str(ctx.channel.id)]["edit"]:
                    if 材料 in materials_list:
                        res = await check_more(ctx.channel.id)
                        data = await get(ctx.channel.id)
                        data["materials"][材料] = 數量
                        res = await put(ctx.channel.id, data)
                        await ctx.send(embed=discord.Embed(title=f"成功申請材料:`{材料}` `{數量}組`",
                                                           description="接下來可以繼續申請材料或使用`/查看目前申請材料`以查看目前已經申請的材料或`/遞交申請`以提交申請給管理員",
                                                           color=discord.Colour.green(),
                                                           timestamp=datetime.datetime.utcnow()).set_author(
                            name=ctx.author, icon_url=ctx.author.avatar_url))
                    elif 材料 in not_materials_list:
                        await ctx.send(embed=discord.Embed(title="你所輸入的材料不在可申請的方塊內",
                                                           description="請到<#858236310744989696>查看可以申請的方塊",
                                                           color=discord.Colour.red(),
                                                           timestamp=datetime.datetime.utcnow()).set_author(
                            name=ctx.author, icon_url=ctx.author.avatar_url))
                    else:
                        await ctx.send(embed=discord.Embed(title="你所輸入的材料名稱不正確或不在可申請的方塊內",
                                                           description="請到<#858236310744989696>查看可以申請的方塊名稱",
                                                           color=discord.Colour.red(),
                                                           timestamp=datetime.datetime.utcnow()).set_author(
                            name=ctx.author, icon_url=ctx.author.avatar_url))
                else:
                    await ctx.send(embed=discord.Embed(title="這個頻道已經遞交了申請", description="若是錯誤遞交或想更改內容請找管理員",
                                                       color=discord.Colour.red(),
                                                       timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                        icon_url=ctx.author.avatar_url))
            else:
                await ctx.send(embed=discord.Embed(title="這個頻道還未申請", description="輸入指令:`/開始申請材料` 以申請小組",
                                                   color=discord.Colour.red(),
                                                   timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                    icon_url=ctx.author.avatar_url))
        else:
            pass

    @commands.command(name="查看目前申請材料")
    async def 查看目前申請材料(self, ctx):
        if ctx.channel.id not in not_channel:
            data = await get_all()
            if str(ctx.channel.id) in data["user"]:
                if data['user'][str(ctx.channel.id)]["edit"]:
                    res = await check_more(ctx.channel.id)
                    data = await get(ctx.channel.id)
                    msg, total = "```\n", 0
                    for materials in data["materials"]:
                        msg = msg + f"{materials} {data['materials'][materials]}組\n"
                        total += data["materials"][materials]
                    bags = ceil(total)
                    msg = msg + f"\n總計{total}組\n需要{bags}個鑽製包包```"
                    await ctx.send(embed=discord.Embed(title=f"`{data['user'][str(ctx.channel.id)]['name']}`目前申請了的材料有:",
                                                       description="接下來可以`/新增申請材料`以繼續申請材料或`/遞交申請`以提交申請給管理員",
                                                       color=discord.Colour.green(),
                                                       timestamp=datetime.datetime.utcnow()).add_field(
                        name="==================================================", value=msg, inline=True).set_author(
                        name=ctx.author, icon_url=ctx.author.avatar_url))
                else:
                    await ctx.send(embed=discord.Embed(title="這個頻道已經遞交了申請", description="若是錯誤遞交或想更改內容請找管理員",
                                                       color=discord.Colour.red(),
                                                       timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                        icon_url=ctx.author.avatar_url))
            else:
                await ctx.send(embed=discord.Embed(title="這個頻道還未申請", description="輸入指令:`/開始申請材料` 以申請小組",
                                                   color=discord.Colour.red(),
                                                   timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                    icon_url=ctx.author.avatar_url))
        else:
            pass

    @commands.command(name="查看目前申請材料")
    async def 遞交申請(self, ctx):
        if ctx.channel.id not in not_channel:
            all_data = await get_all()
            if str(ctx.channel.id) in all_data["user"]:
                if all_data['user'][str(ctx.channel.id)]["edit"]:
                    res = await check_more(ctx.channel.id)
                    data = await get(ctx.channel.id)
                    awa, total = "```\n", 0
                    for materials in data["materials"]:
                        awa = awa + f"{materials} {data['materials'][materials]}組\n"
                        total += data["materials"][materials]
                    bags = ceil(total)
                    awa = awa + f"\n總計{total}組\n需要{bags}個鑽製包包```"
                    awa = await ctx.send(embed=discord.Embed(title="確定遞交申請?",
                                                             description=f"`{data['name']}`目前申請了的材料有:\n{awa}\n如確認上述資料無誤，請在三十秒內輸入`確定`遞交申請\n注：提交申請後無法更改",
                                                             color=discord.Colour.green()).set_author(name=ctx.author,
                                                                                                      icon_url=ctx.author.avatar_url))
                    try:
                        def check(message):
                            return message.author.id == ctx.author.id

                        message = await self.client.wait_for("message", check=check, timeout=30)
                    except asyncio.TimeoutError:
                        await ctx.send(
                            embed=discord.Embed(title="已取消遞交申請", description="原因：操作過時(三十秒)", color=discord.Colour.red(),
                                                timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                 icon_url=ctx.author.avatar_url))
                        await awa.delete()
                        return
                    if message.content == "確定":
                        awa.delete()
                        message.delete()
                        data["edit"] = False
                        send_msg = await self.client.get_channel(865180618634821632).send(
                            embed=discord.Embed(title=f"`{data['user'][str(ctx.channel.id)]['name']}`遞交了申請：",
                                                description=f"申請人:<@!{ctx.author.id}>", color=0xfffff9,
                                                timestamp=datetime.datetime.utcnow()).set_author(
                                name=ctx.author).add_field(name="申請建造材料:", value=awa).set_footer(text="Stage: 1"))
                        all_data["data"][str(message.id)] = {"channel_id": ctx.channel.id, "stage": 1,
                                                             "user_id": ctx.author.id}
                        data["message_id"] = send_msg.id
                        res = await put_all(all_data)
                        res = await put(ctx.channel.id, data)
                        for emoji in ["✅", "❌", "💬", "#️⃣"]:
                            await send_msg.add_reaction(emoji)
                        await ctx.sned(
                            embed=discord.Embed(title="這個頻道的材料申請已經成功遞交", description="審核完成後會有通知，請耐心等待",
                                                color=discord.Colour.green(),
                                                timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                 icon_url=ctx.author.avatar_url).set_footer(
                                text="此訊息由機器人發送，請不要回覆訊息").add_field(name="你所申請的材料:", value=awa, inline=True))
                    else:
                        await awa.delete()
                        await message.delete()
                        await ctx.send(embed=discord.Embed(title="已取消遞交申請", color=discord.Colour.red(),
                                                           timestamp=datetime.datetime.utcnow()).set_author(
                            name=ctx.author, icon_url=ctx.author.avatar_url))
                else:
                    await ctx.send(embed=discord.Embed(title="這個頻道已經遞交了申請", description="若是錯誤遞交或想更改內容請找管理員",
                                                       color=discord.Colour.red(),
                                                       timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                        icon_url=ctx.author.avatar_url))
            else:
                await ctx.send(embed=discord.Embed(title="這個頻道還未申請", description="輸入指令:`/開始申請材料` 以申請小組",
                                                   color=discord.Colour.red(),
                                                   timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                    icon_url=ctx.author.avatar_url))
        else:
            pass

    @commands.command(name="撤回遞交申請")
    async def 撤回遞交申請(self, ctx):
        if ctx.channel.id not in not_channel:
            all_data = await get_all()
            if str(ctx.channel.id) in all_data["user"]:
                if not all_data['user'][str(ctx.channel.id)]["edit"]:
                    res = await check_more(ctx.channel.id)
                    data = await get(ctx.channel.id)
                    msg = await ctx.send(embed=discord.Embed(title="確定撤回遞交申請?", description=f"如確認，請在三十秒內輸入`確定`",
                                                             color=discord.Colour.green()).set_author(name=ctx.author,
                                                                                                      icon_url=ctx.author.avatar_url))
                    try:
                        def check(message):
                            return message.author.id == ctx.author.id

                        message = await self.client.wait_for("message", check=check, timeout=30)
                    except asyncio.TimeoutError:
                        await ctx.send(
                            embed=discord.Embed(title="已取消遞交申請", description="原因：操作過時(三十秒)", color=discord.Colour.red(),
                                                timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                 icon_url=ctx.author.avatar_url))
                        await msg.delete()
                        return
                    if message.content == "確定":
                        data["edit"] = True
                        send_mg = await self.client.get_channel(865180618634821632).fetch_message(
                            all_data["user"][str(ctx.channel.id)]["message_id"])
                        await send_mg.edit(
                            embed=discord.Embed(title=f"此申請(`{data['user'][str(ctx.channel.id)]['name']}`)已被撤回",
                                                description=f"撤回者:<@!{ctx.author.id}>", color=0xfffff9,
                                                timestamp=datetime.datetime.utcnow()))
                        await send_mg.clear_reactions()
                        await send_mg.add_reaction("🆗")
                        await send_mg.add_reaction("💬")
                        data["data"].pop(str(send_mg.id), None)
                        data.pop("message_id", None)
                        all_data["wait"].append(message.id)
                        res = await put_all(all_data)
                        res = await put(ctx.channel.id, data)
                        await ctx.send(
                            embed=discord.Embed(title="這個頻道的材料申請已經成功撤回", description="", color=discord.Colour.green(),
                                                timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                 icon_url=ctx.author.avatar_url))
                    else:
                        await msg.delete()
                        await message.delete()
                        await ctx.send(embed=discord.Embed(title="已取消遞交申請", color=discord.Colour.red(),
                                                           timestamp=datetime.datetime.utcnow()).set_author(
                            name=ctx.author, icon_url=ctx.author.avatar_url))
                else:
                    await ctx.send(embed=discord.Embed(title="這個頻道還沒有遞交申請", description="", color=discord.Colour.red(),
                                                       timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                        icon_url=ctx.author.avatar_url))
            else:
                await ctx.send(embed=discord.Embed(title="這個頻道還未申請", description="輸入指令:`/開始申請材料` 以申請小組",
                                                   color=discord.Colour.red(),
                                                   timestamp=datetime.datetime.utcnow()).set_author(name=ctx.author,
                                                                                                    icon_url=ctx.author.avatar_url))
        else:
            pass


def setup(client):
    client.add_cog(get_materials_command(client))

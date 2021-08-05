import asyncio
from cogs.core import core
from cogs.functions import get_all, get, put, put_all
from discord.ext import commands
from math import ceil
import discord
import datetime


class on_raw_reaction_add(core):

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if str(payload.emoji) in ["☑️", "🇽", "🆗", "💬", "#️⃣",
								"👍"] and not payload.member.bot and payload.channel_id == 865180618634821632:
			all_data = await get_all()
			if str(payload.message_id) in all_data["data"]:
				message = await self.client.get_channel(865180618634821632).fetch_message(payload.message_id)
				channel = self.client.get_channel(all_data["data"][str(message.id)]["channel_id"])
				if payload.message_id in all_data["wait"] and payload.emoji.name == "🆗":
					await message.clear_reactions()
					await message.add_reaction("✅")
					await message.add_reaction("❌")

					def check(newPayload):
						return newPayload.member.id == payload.member.id and str(newPayload.emoji.name) in ["✅", "❌"]

					newPayload = await self.client.wait_for("raw_reaction_add", check=check)
					if str(newPayload.emoji.name) == "✅":
						await message.delete()
						all_data["wait"].remove(payload.message_id)
						all_data["data"].pop(str(message.id), None)
						await put_all(all_data)
					if str(newPayload.emoji.name) == "❌":
						await message.clear_reactions()
						await message.add_reaction("🆗")
						await message.add_reaction("💬")
				elif str(payload.emoji) == "💬":
					msg2 = await self.client.get_channel(865180618634821632).send("輸入訊息: (輸入`-`取消發送)")
					msg = await self.client.wait_for("message",
													check=lambda message: message.author == payload.member)
					if msg.content != "-":
						embed = discord.Embed(title="",
											description=f"<@!{payload.user_id}>:\n```\n{msg.content}\n```",
											color=0xfffff9, timestamp=datetime.datetime.utcnow())
						await self.client.get_channel(all_data["data"][str(payload.message_id)]["channel_id"]).send(
							embed=embed)
						await msg.delete()
						await msg2.delete()
						await message.remove_reaction("💬", payload.member)
					else:
						await msg.delete()
						await msg2.delete()
						await message.remove_reaction("💬", payload.member)
				elif str(payload.emoji) == "#️⃣":
					send_msg = await self.client.get_channel(865180618634821632).send(
						"輸入訊息: (輸入`-`取消註記，輸入`.`刪除原有註記，新的註記會覆蓋舊有的)")

					if "note" in all_data["data"][str(payload.message_id)]:
						text = all_data["data"][str(payload.message_id)]["note"]
						msg1 = await self.client.get_channel(865180618634821632).send(
							embed=discord.Embed(title="上次註記：", description=f"```{text}```", color=0xfffff9))

					get_message = await self.client.wait_for("message",
															check=lambda m: m.author.id == payload.member.id)

					if get_message.content == "-":
						await send_msg.delete()
						await get_message.delete()
						if "note" in all_data["data"][str(payload.message_id)]:
							await msg1.delete()
						await message.remove_reaction("#️⃣", payload.member)
					elif get_message.content == ".":
						await send_msg.delete()
						await get_message.delete()
						if "note" in all_data["data"][str(payload.message_id)]:
							await msg1.delete()
						embed = message.embeds[0]
						if embed.fields[1].name == "註記：":
							embed.remove_field(1)
						all_data["data"][str(payload.message_id)].pop("note", None)
						await put_all(all_data)
						await message.edit(embed=embed)
						await message.remove_reaction("#️⃣", payload.member)
					else:
						await send_msg.delete()
						await get_message.delete()
						if "note" in all_data["data"][str(payload.message_id)]:
							await msg1.delete()
						embed = message.embeds[0]
						if "note" in all_data["data"][str(payload.message_id)]:
							if embed.fields[1].name == "註記：":
								embed.remove_field(1)
						all_data["data"][str(payload.message_id)]["note"] = str(get_message.content)
						embed.add_field(name="註記：", value=f"```\n{get_message.content}\n```", inline=False)
						await put_all(all_data)
						await message.edit(embed=embed)
						await message.remove_reaction("#️⃣", payload.member)

				elif all_data["data"][str(payload.message_id)]["stage"] == 1:
					if str(payload.emoji) == "☑️":
						await channel.send(
							embed=discord.Embed(title="材料申請通過\n我們正在準備材料，準備好會有通知",
												description=f"處理者:<@!{payload.user_id}>",
												color=discord.Colour.green(), timestamp=datetime.datetime.utcnow()))
						channel_id = all_data['data'][str(payload.message_id)]['channel_id']
						data = await get(channel_id)
						ready, total = "```\n", 0
						for materials in data["materials"]:
							ready = ready + f"{materials} {data['materials'][materials]}組\n"
							total += data["materials"][materials]
						bags = ceil(total/54)
						ready = ready + f"\n總計{total}組\n需要{bags}個鑽製包包```"

						if "note" in all_data["data"][str(payload.message_id)]:
							ready = ready + "\n註記：\n```" + all_data["data"][str(payload.message_id)]["note"] + "```"
						embed = discord.Embed(title=f"`{data['name']}`遞交了申請： (準備中)",
											description=f"申請人:<@!{all_data['data'][str(payload.message_id)]['user_id']}>",
											color=discord.Colour.green(),
											timestamp=datetime.datetime.utcnow()).add_field(name="請準備材料:",
																							value=ready,
																							inline=True).set_footer(
							text="Stage: 2")
						await message.edit(embed=embed)
						await message.clear_reactions()
						await message.add_reaction("👍")
						await message.add_reaction("💬")
						await message.add_reaction("#️⃣")
						all_data["data"][str(payload.message_id)]["stage"] = 2
						await put_all(all_data)
						await put(channel_id, data)
					elif payload.emoji.name == "🇽":
						msg2 = await self.client.get_channel(865180618634821632).send("不通過的原因:(輸入`-`取消發送)")
						msg = await self.client.wait_for("message",
														check=lambda m: m.author == payload.member)
						if str(msg.content) != "-":
							await channel.send(
								embed=discord.Embed(title="材料申請不通過", description=f"處理者:<@!{payload.user_id}>",
													color=discord.Colour.red(),
													timestamp=datetime.datetime.utcnow()).add_field(name="不通過原因:",
																									value=f"```{msg.content}```",
																									inline=True))
							channel_id = all_data['data'][str(payload.message_id)]['channel_id']
							embed = discord.Embed(title=f"已拒絕`{all_data['user'][str(channel_id)]['name']}`的申請",
												description=f"處理者:<@!{payload.user_id}>", color=0xfffff9,
												timestamp=datetime.datetime.utcnow())
							await message.edit(embed=embed)
							await msg.delete()
							await msg2.delete()
							await message.clear_reactions()
							await message.add_reaction("🆗")
							await message.add_reaction("💬")
							all_data["data"][str(message.id)]["stage"] = 0
							all_data["user"][str(channel_id)].pop("message_id", None)
							all_data["wait"].append(message.id)
							all_data['user'][str(channel_id)]["edit"] = True
							await put_all(all_data)
						else:
							await msg.delete()
							await msg2.detele()
							await message.remove_reaction("❌", payload.member)
				elif all_data["data"][str(payload.message_id)]["stage"] == 2:
					if str(payload.emoji) == "👍":
						await message.clear_reactions()
						await message.add_reaction("✅")
						await message.add_reaction("❌")
						try:
							newPayload = await self.client.wait_for("raw_reaction_add", check=lambda
								p: p.member.id == payload.member.id and str(p.emoji) in ["✅", "❌"], timeout=30)
						except asyncio.TimeoutError:
							await message.clear_reactions()
							await message.add_reaction("👍")
							await message.add_reaction("💬")
							await message.add_reaction("#️⃣")
							return
						if str(newPayload.emoji) == "✅":
							await message.clear_reactions()

							embed = message.embeds[0]
							embed.title = f"`{all_data['user'][str(channel.id)]['name']}`遞交了申請： (待領取)"
							embed.set_footer(text = "Stage: 3")
							embed.color = 0x00bfff


							await channel.send(embed=discord.Embed(title="材料已準備好\n請自備包包至/to !ARTC! 3F找管理員領取",
																description=f"處理者:<@!{payload.member.id}>",
																color=0xfcfc00,
																timestamp=datetime.datetime.utcnow()).add_field(name="材料:	", value=embed.fields[0].value))

							await message.edit(embed=embed)
							await message.clear_reactions()
							await message.add_reaction("🆗")
							await message.add_reaction("💬")
							all_data["data"][str(message.id)]["stage"] = 0
							all_data["user"].pop(str(channel.id), None)
							all_data["wait"].append(message.id)
							await put_all(all_data)
						elif str(newPayload.emoji) == "❌":
							await message.clear_reactions()
							await message.add_reaction("👍")
							await message.add_reaction("💬")
							await message.add_reaction("#️⃣")


def setup(client):
	client.add_cog(on_raw_reaction_add(client))

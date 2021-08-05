import discord


embed = discord.Embed(title="awa").add_field(name="1", value="awa", inline=True)


print(embed.fields[0].name)


embed.remove_field(0)

print(embed.fields)

embed.title = "aw"

print(embed.title)

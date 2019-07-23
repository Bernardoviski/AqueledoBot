import discord
import asyncio
from discord.ext.commands import *
from essential import *
import datetime
import os
from discord import Embed


class Commands(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="ping", aliases=["online"])
	async def online(self, ctx):
		await ctx.send(f"🏓 Pong  `{int(round(self.bot.latency*1000, 2))} ms`")

	@command(name='level', aliases=["levels", "xp", "nivel"])
	async def level(self, ctx):
		data = Database(ctx.message.author.id).get()
		level, xp = (data["level"], data["xp"])
		embed = Embed(title='Níveis', timestamp=datetime.datetime.today(), description='', color=0xFDDFDF)
		embed.set_thumbnail(url=ctx.message.author.avatar_url)
		embed.add_field(name="Nível", value=level)
		embed.add_field(name="XP", value=xp)
		embed.add_field(name="XP para o Próximo nível ", value=(level * 100)-xp)
		await ctx.send(embed=embed)
	
def setup(bot):
	bot.add_cog(Commands(bot))

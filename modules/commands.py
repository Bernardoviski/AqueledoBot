import discord
import asyncio
from discord.ext.commands import *
from essential import *
import datetime
import os


class Commands(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="ping", aliases=["online"])
	async def online(self, ctx):
		print("Recieved on ping")
		await ctx.send(f"ðŸ“ Pong  `{int(round(self.bot.latency*1000, 2))} ms`")
		print("Ping Done")

	@command(name='level')
	async def level(self, ctx):
		data = Database(ctx.message.author.id).get()
		level, xp = (data["level"], data["xp"])
		await ctx.send(f"LEVEL: {level} | XP: {xp}")


def setup(bot):
	bot.add_cog(Commands(bot))

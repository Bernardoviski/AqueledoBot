import discord, asyncio
from discord.ext.commands import Cog
from essential import *
import datetime
import threading
class Events(Cog):
	def __init__(self, bot):
		self.bot = bot
	@Cog.listener()
	async def on_ready(self):
		log("Connected and ready.", 1)
		log(f"Ping: {int(round(self.bot.latency*1000, 2))}ms", 1)
		console_thread = threading.Thread(target=console, args=(None, self.bot), daemon=True)
		console_thread.start()
	@Cog.listener()
	async def on_command(self, ctx):
		log(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] [{ctx.guild.name}] {ctx.message.author}: {ctx.message.content}", 1)
#	
def setup(bot):
	bot.add_cog(Events(bot))
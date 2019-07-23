from discord.ext.commands import Cog
from essential import *
from time import time
import threading


def Message_Handler(message, database):
	data = database.get()
	if time() - data["unix"] > 20 and data["last_message"] != message.content:
		level = data["level"]
		xp = round(data["xp"] + (time() - data["unix"])/(data["level"]*0.5)*0.3)
		if xp > 50: xp = 50
		while (xp >= level * 100):
			level += 1			
			xp = xp-(data["level"]*100)
		database.edit("level", level)
		database.edit("xp", xp)
		database.edit("unix_lastmessage", time())
		database.edit("lastmessage", message.content)
		database.close()


class Events(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_message(self, message):
		if not message.author.bot:
			thread = threading.Thread(
				target=Message_Handler,
				args=(message, Database(message.author.id)),
				daemon=True
			)
			thread.start()


def setup(bot):
	bot.add_cog(Events(bot))
	
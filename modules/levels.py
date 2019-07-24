from discord.ext.commands import Cog
from essential import *
from time import time
import threading


async def Message_Handler(message, database):
	data = database.get()
	if time() - data["unix"] > 20 and data["last_message"] != message.content:

		xp = data["xp"]
		level = data["level"]
		last_message_time = data["unix"]
		xp_to_add = round((time()-last_message_time)/level)
		if xp_to_add > 49:
			xp_to_add = 49
		
		total_xp = xp + xp_to_add
		
		if total_xp > level*100:
			total_xp -= level*100
			level += 1

		if level != data["level"]:
			
			database.edit("level", level)
			
		database.edit("unix_lastmessage", time())
		database.edit("xp", total_xp)	
		database.edit("lastmessage", message.content)
		database.close()
		role = LevelManager(level).getrole()
		if role:
			await message.author.add_roles(message.guild.get_role(role))

class Events(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_message(self, message):
		if not message.author.bot:
			await Message_Handler(message, Database(message.author.id))


def setup(bot):
	bot.add_cog(Events(bot))
	
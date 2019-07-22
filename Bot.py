from colorama import init as init_colorama
from essential import *
from sys import stdout
import traceback
from discord.ext import commands
import discord
import threading

global bot
init_colorama()
config = Config()
bot = commands.Bot(command_prefix=config.prefix, owner_id=config.owner)
bot.remove_command("help")
log("Loading Modules.", 1)
for module_file in config.modules:
	try:
		bot.load_extension(module_file)
		log(f"Module {module_file} loaded with no errors", 2)
	except Exception as e:
		log(f"Module {module_file} failed to load ({e})", 4)
		print(f"{Fore.RED}")
		traceback.print_exc(file=stdout)
		print(f"{Fore.RESET}")
try:
	bot.run(config.token, bot=True, reconnect=True)
except Exception as e:
	log(f'Failed to start-up. ({e})', 5)
	print(f"{Fore.RED}")
	traceback.print_exc(file=stdout)
	print(f"{Fore.RESET}")
	exit()

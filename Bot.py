from colorama import Fore, Back, Style
from colorama import init as init_colorama
from essential import *
from sys import stdout
import traceback
from discord.ext import commands
import discord
import threading
init_colorama()
config = Config()
database = Database()
bot = commands.Bot(command_prefix=config.prefix, owner_id=config.owner)

# Uso do LOG
# 1 - Info
# 2 - Sucesso
# 3 - Aviso
# 4 - Falha
# 5 - Erro Critico

def log(text, type: int):
	output = ""
	if type == 1:
		output = f"[ INFO ] {text}"
	elif type == 2:
		output = f"[{Back.GREEN}{Fore.WHITE}{Style.BRIGHT} LOG {Fore.RESET}{Back.RESET}] {text}"
	elif type == 3:
		output = f"[ WARN ] {text}"
	elif type == 4:
		output = f"[{Back.RED}{Fore.WHITE}{Style.BRIGHT} FAIL {Fore.RESET}{Back.RESET}] {text}"
	elif type == 5:
		output = f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}////////////{Back.RESET}{Fore.RED} ERROR {Fore.RESET}{Back.RED}{Fore.WHITE}{Style.BRIGHT}\\\\\\\\\\\\\\\\\\\\\\\\{Fore.RESET}{Back.RESET}".center(400)+f"\n{Fore.RED}{Style.DIM}{text} {Fore.RESET}"
	else:
		raise(ValueError)
		return
	print(output)

try:
	bot.run(config.token2, bot=True, reconnect=True)
except Exception as e:
	log(f'Failed to start-up. ({e})\n\n\n\n\n', 5)
	traceback.print_exc(file=stdout)
	exit()

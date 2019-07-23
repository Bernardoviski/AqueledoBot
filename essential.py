from os import listdir
from json import load
from colorama import Fore, Back, Style
from colorama import init as init_colorama
from os import _exit
import traceback
from sys import stdout
import asyncio
import pymysql
import threading
from time import time


class Database_Connection_Closed(Exception):
	def __init__(self):
		pass


class Database(object):
	def __init__(self, user_id):
		self.user = user_id
		_config = Config()
		self.closed = False
		self.table = _config.database_table
		self.connection = pymysql.connect(
			host=_config.database_host,
			port=_config.database_port,
			user=_config.database_user,
			passwd=_config.database_password,
			db=_config.database_name
		)

	def get(self):
		cursor = self.connection.cursor()

		try:
			if self.closed:
				raise(Database_Connection_Closed)
				exit()

			cursor.execute(f"SELECT * FROM `{self.table}` WHERE `user` = '{self.user}'")
			row = [row for row in cursor][0]
			return {"unix": row[0], "last_message": row[1], "level": row[2], "xp": row[3]}

		except IndexError:
			print(f"INSERT INTO `users` (`unix_lastmessage`, `lastmessage`, `level`, `xp`, `user`) VALUES ('{time()}', '', '1', '0', '{self.user}')")
			cursor.execute(f"INSERT INTO `users` (`unix_lastmessage`, `lastmessage`, `level`, `xp`, `user`) VALUES ('{time()}', '', '1', '0', '{self.user}')")
			self.connection.commit()
			return {"unix": time(), "last_message": '', "level": 1, "xp": 0}

		else:
			log(f"Failed to edit the database.\n({error})", 5)
			print(f"{Fore.RED}\n"+'-'*100)			
			traceback.print_exc(file=stdout)
			print(('-'*100)+f"{Fore.RESET}")

	def edit(self, col, value):
		try:
			if self.closed:
				raise(Database_Connection_Closed)
				exit()

			cursor = self.connection.cursor()
			cursor.execute(f"UPDATE `{self.table}` SET `{col}` = '{value}' WHERE `user` = '{self.user}'")
			self.connection.commit()
			print("Sent - FROM ESSENTIAL -")

		except Exception as error:
			log(f"Failed to edit the database.\n({error})", 5)
			print(f"{Fore.RED}\n"+'-'*100)			
			traceback.print_exc(file=stdout)
			print(('-'*100)+f"{Fore.RESET}")

	def create(self):
		try:
			if self.closed:
				raise(Database_Connection_Closed)
				exit()

			cursor = self.connection.cursor()
			cursor.execute(f"INSERT INTO `users` (`unix_lastmessage`, `lastmessage`, `level`, `xp`, `user`) VALUES ('{time()}', '', '1', '0', '{self.user}')")
			self.connection.commit()

		except Exception as error:
			log(f"Failed to edit the database.\n({error})", 5)
			print(f"{Fore.RED}\n"+'-'*100)			
			traceback.print_exc(file=stdout)
			print(('-'*100)+f"{Fore.RESET}")

	def close(self):
		self.connection.close()
		self.closed = True
	
class Config(object):
	def __init__(self, config_file: str = 'config.json'):
		config_contents = load(open(config_file, 'r'))
		self.prefix = config_contents['prefix']
		self.owner = config_contents['owner']
		self.token = config_contents['token']
		self.database_host = config_contents['database']["host"]
		self.database_port = config_contents['database']["port"]
		self.database_user = config_contents['database']["user"]
		self.database_name = config_contents['database']["database_name"]
		self.database_table = config_contents['database']["table"]
		self.database_password = config_contents['database']["password"]
		self.database = config_contents['database']
		if config_contents['modules']['auto-find']:
			self.modules = [f"modules.{file}"[:-3] for file in listdir('modules') if file.endswith('.py') and (not file.startswith("-"))]	
		else:		
			self.modules = [f"modules.{file}" for file in config_contents['modules']['list']]


def console(dummy, bot):
	log("Starting terminal.", 1)
	loop = False

	while True:
		try:
			if not loop:
				log("Terminal Started.", 2)
				loop = True

			commando = input("£ ")
			if commando.lower() in ["stop", "shutdown"]:
				log("Shutdown issued by Terminal", 6, 'STOP')
				_exit(0)

			elif commando.lower() in ["reload"]:
				log("Reloading Modules.", 1)
				modules = Config().modules
				for module in modules:
					try:
						bot.load_extension(module)
					except:
						pass

				for module in modules:
					try:
						bot.unload_extension(module)
						bot.load_extension(module)
						log(f"Module {module} loaded with no errors", 2)
					except Exception as e:
						log(f"Module {module} failed to load ({e})", 4)
						print(f"{Fore.RED}")
						traceback.print_exc(file=stdout)
						print(f"{Fore.RESET}")

			else:
				log("Available Commands: shutdown, reload", 3)

		except Exception as e:
			log(f"Terminal failed to comply the command.\n({e})", 5)
			print(f"{Fore.RED}\n"+'-'*100)
			traceback.print_exc(file=stdout)
			print(('-'*100)+f"{Fore.RESET}")


def log(text, type: int, title=None):
	output = ""
	if type == 1:
		output = f"[ INFO ] {text}"

	elif type == 2:
		output = f"[{Back.GREEN}{Fore.WHITE}{Style.BRIGHT} OK {Fore.RESET}{Back.RESET}] {text}"

	elif type == 3:
		output = f"[ WARN ] {text}"
	
	elif type == 4:
		output = f"[{Back.RED}{Fore.WHITE}{Style.BRIGHT} FAIL {Fore.RESET}{Back.RESET}] {text}"
	
	elif type == 5:
		output = f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}////////////{Back.RESET}{Fore.RED} ERROR {Fore.RESET}{Back.RED}{Fore.WHITE}{Style.BRIGHT}\\\\\\\\\\\\\\\\\\\\\\\\{Fore.RESET}{Back.RESET}".center(400)+f"\n{Fore.RED}{Style.DIM}{text} {Fore.RESET}"
	
	elif type == 6:
		output = f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}////////////{Back.RESET}{Fore.RED} {title} {Fore.RESET}{Back.RED}{Fore.WHITE}{Style.BRIGHT}\\\\\\\\\\\\\\\\\\\\\\\\{Fore.RESET}{Back.RESET}".center(400)+f"\n{Fore.RED}{Style.DIM}{text} {Fore.RESET}"
	
	else:
		raise(ValueError)
		return

	print(output)

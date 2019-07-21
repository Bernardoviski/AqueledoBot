from os import listdir
from json import load

class Config(object):
	def __init__(self, config_file: str = 'config.json'):
		config_contents = load(open(config_file, 'r'))
		self.prefix = config_contents['prefix']
		self.owner = config_contents['owner']
		self.token = config_contents['token']
		
		if config_contents['modules']['auto-find']:
			self.modules = [file for file in listdir('modules') if file.endswith('.py') and (not file.startswith("-"))]	
		else:		
			self.modules = config_contents['modules']['list']

class Database(object):
	def __init__(self):
		pass

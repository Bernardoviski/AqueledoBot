import asyncio
from discord.ext.commands import *
from essential import *
import datetime
import os
from discord import Embed, Role


class Commands(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="ping", aliases=["online"])
	async def online(self, ctx):
		await ctx.send(f"🏓 Pong  `{int(round(self.bot.latency*1000, 2))} ms`")
	@command(name="setrole", aliases=["levelrole"])
	@has_permissions(administrator=True)
	async def setrole(self, ctx, level: int = None, role: Role = None):
		if level and role:
			level_manager = LevelManager(level)
			level_manager.setrole(role.id)
			embed = Embed(title='Operação Concluida ✅', timestamp=datetime.datetime.today(), description='Operação Concluida com sucesso', color=0x00cd00)
		else:
			embed = Embed(title='Falha ', timestamp=datetime.datetime.today(), description='Uso Correto: !setrole [Nível] [Role]', color=0xb20000)
		await ctx.send(embed=embed)
	@command(name="clearrole", aliases=["levelroleclear"])
	@has_permissions(administrator=True)
	async def deleterole(self, ctx, level: int = None):
		if level:
			level_manager = LevelManager(level)
			level_manager.removerole()
			embed = Embed(title='Operação Concluida ✅', timestamp=datetime.datetime.today(), description='Operação Concluida com sucesso', color=0x00cd00)
		else:
			embed = Embed(title='Falha ', timestamp=datetime.datetime.today(), description='Uso Correto: !clearrole [Nível]', color=0xb20000)
		await ctx.send(embed=embed)
	@command(name="listroles", aliases=["levelrolelist", "lrl"])
	@has_permissions(administrator=True)
	async def listroles(self, ctx):
		all_roles = LevelManager(0).getall()
		embed = Embed(title='Operação Concluida ✅', timestamp=datetime.datetime.today(), description='Pesquisa executada com sucesso.', color=0x00cd00)
		for level in all_roles:
			embed.add_field(name=f"Nível {level}", value=f"Role: <@&{all_roles[str(level)]['role']}>")
		await ctx.send(embed=embed)
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

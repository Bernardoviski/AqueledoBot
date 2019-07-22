import random
from discord.ext.commands import *
from discord.ext import commands
import discord
import datetime
from essential import *


ErrorTitles = ['Ops!', 'Falhou aqui', 'Eita!', 'Oshi!', 'Erro!', 'Vish...']


class errorHanlder(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_command_error(self, ctx, error):	
		error = getattr(error, 'original', error)
		log("Um erro ocorreu ao executar um comando.", 1)
		log(f"Detalhes:\nUser: {ctx.author}\nMensagem: {ctx.message.content}\nGuild: {ctx.guild.name}\nErro: {error}", 1)

		if isinstance(error, (commands.MissingRequiredArgument, commands.TooManyArguments, commands.BadArgument)):
			usage = await utils.format_usage(ctx)
			embed = discord.Embed(title='Uso correto:', timestamp=datetime.datetime.today(), description=usage, color=0xF01010)

		elif str(error) == "BAD REQUEST (status code: 400): You can only bulk delete messages that are under 14 days old.":
			embed = discord.Embed(title=random.choice(ErrorTitles), timestamp=datetime.datetime.today(), description=f'Parece que eu não posso deletar mensagens que tem mais de 14 dias de existencia... :/', color=0xcc0000)

		elif isinstance(error, commands.CommandNotFound):
			embed = discord.Embed(title=random.choice(ErrorTitles), timestamp=datetime.datetime.today(), description=f'Este comando não existe', color=0xcc0000)

		elif isinstance(error, commands.NoPrivateMessage):
			embed = discord.Embed(title=random.choice(ErrorTitles), timestamp=datetime.datetime.today(), description=f'Este comando só funciona em guilds', color=0xcc0000)

		elif isinstance(error, commands.DisabledCommand):
			embed = discord.Embed(title=random.choice(ErrorTitles), timestamp=datetime.datetime.today(), description=f'Este comando foi desabilitado', color=0xcc0000)

		elif isinstance(error, commands.NotOwner):
			embed = discord.Embed(title=random.choice(ErrorTitles), timestamp=datetime.datetime.today(), description=f'Você não pode executar este comando.', color=0xcc0000)

		elif isinstance(error, commands.CheckFailure):
			embed = discord.Embed(title=random.choice(ErrorTitles), timestamp=datetime.datetime.today(), description=f'Você não pode executar este comando.', color=0xcc0000)

		elif isinstance(error, commands.MissingPermissions):
			embed = discord.Embed(title=random.choice(ErrorTitles), timestamp=datetime.datetime.today(), description=f'Você não tem as permissões necessárias', color=0xcc0000)
			embed.add_field(name="Permissões", value=', '.join(perm for perm in error.missing_perms))

		elif isinstance(error, commands.MissingPermissions):
			embed = discord.Embed(title=random.choice(ErrorTitles), timestamp=datetime.datetime.today(), description=f'Eu não tenho as permissões necessárias', color=0xcc0000)
			embed.add_field(name="Permissões", value=', '.join(perm for perm in error.missing_perms))		
			
		else:
			embed = discord.Embed(title=random.choice(ErrorTitles), timestamp=datetime.datetime.today(), description=f'Algo deu errado.', color=0xcc0000)
			print(error)

		return await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(errorHanlder(bot))
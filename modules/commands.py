import discord, asyncio
from discord.ext.commands import *
from essential import *
import datetime, os, ast



class Commands(Cog):
	def __init__(self, bot):
		self.bot = bot
	@command(name="ping", aliases=["online"])
	async def online(self, ctx):		
		await ctx.send(f"ðŸ“ Pong  `{int(round(self.bot.latency*1000, 2))} ms`")
	@command(name='eval')
	@is_owner()
	async def eval(self, ctx,  *, code: str):
		FN_NAME = '_eval_expr'
		code_lines = code.splitlines()
		if code_lines[0].startswith('```') and code_lines[-1].endswith('```'):
			code = code[len(code_lines[0]):-len(code_lines[-1])]
			code_lines = code_lines[1:-1]
		indented_code = '\n'.join([f'	{i}' for i in code_lines])
		body = (f'async def {FN_NAME}():\n{indented_code}')
		embed = discord.Embed(color=0x10E010, timestamp=datetime.datetime.today())
		code
		if len(code) > 1000:
			code = code[:1000] + '\n...'
		embed.add_field(name='Código:', value=f'```python\n{code}\n```', inline=False)
		result = None
		try:
			parsed = ast.parse(body)
			body = parsed.body[0].body
		except SyntaxError as error:
			err_code = error.text[4:]
			err_code = err_code.replace('\n', '')
			line_no = error.lineno - 1
			result = f"Syntax error:\n'{err_code}'\n(line {line_no})"
			if len(result) > 1000:
				result = result[:1000] + '\n...'
			embed.add_field(name='Resultado:', value=f'```python\n{result}\n```', inline=False)
			return await ctx.send(embed=embed)
		if isinstance(body[-1], ast.Expr):
			body[-1] = ast.Return(body[-1].value)
		ast.fix_missing_locations(body[-1])
		vars = {
				'bot': self.bot,
				'channel': ctx.channel,
				'ctx': ctx,
				'guild': ctx.guild,
				'voice_client': ctx.voice_client
			}
		vars.update(locals())
		vars.update(globals())
		try:
			exec(compile(parsed, filename='<ast>', mode='exec'), vars)
			result = str(await eval(f'{FN_NAME}()', vars))
		except Exception as ex:
			result = f'{type(ex).__name__}: {ex}'
			embed.color = 0xE01010
		finally:
			if len(result) > 1000:
				result = result[:1000] + '\n...'
			embed.add_field(name='Resultado:', value=f'```python\n{result}\n```', inline=False)
			await ctx.send(embed=embed)
def setup(bot):
	bot.add_cog(Commands(bot))

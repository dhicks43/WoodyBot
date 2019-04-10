import os
import discord
from datetime import datetime
import aiohttp

from discord.ext import commands


class BasicCog:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def kooda(self):
		await self.bot.say("https://www.youtube.com/watch?v=yz7Cn3pHibo")

	@commands.command()
	async def joined(self, *, member: discord.Member):
		await self.bot.say('{0} joined on {0.joined_at}'.format(member))

	@commands.command(pass_context=True)
	async def thread(self, ctx):  # thread_name: str, opening_message: str):
		'''if len(self.bot.server_dict) < 60:
			thread_name = thread_name.replace(" ", "_").lower()
			await self.bot.create_channel(ctx.message.server, thread_name)
			print(self.bot.get_channel(thread_name))'''
		for _ in [_ for _ in self.bot.server_dict[ctx.message.server.name]]:
			for key in _:
				print(self.bot.get_channel(_[key]).type)
		# if self.bot.get_channel(_[key]).type.category == "thread":
		#	print(key)

	@commands.command(name='delete_all', pass_context=True)
	async def delet(self, ctx, *args):
		await self.bot.say('Sure about that boss?')
		msg = await self.bot.wait_for_message(author=ctx.message.author)
		dog = datetime( 2018, 8, 4)
		if msg.content == 'yeet':
			for channel in self.bot.server_dict['Midnight Marauders']:
				for bizza in channel:
					try:
						count = 0
						async for i in self.bot.logs_from(channel[bizza], limit=500_000, before=dog):
							if i.author.name == 'WoodyAllen':
								print('Deleting: ', i)
								await self.bot.delete_message(i)

						print('Deleting', count, 'messages from', bizza)

					except discord.errors.Forbidden:
						print("Don't have acess to " + bizza + "!")

			# working_messages = self.bot.server_dict[channel].history().get(author__name='WoodyAllen')
			# for i in working_messages:
			#	print(i)

			'''while finished_parsing:
				try:
					async for message in working_messages:
						if message.author.name == "WoodyAllen":
							#delet
							print("Message found!")

					more_check = 0
					async for i in self.bot.logs_from(self.bot.get_channel(channel_list[channel]), before=last_message,
												  limit=10):
						more_check += 1

					if more_check > 0:
						print("Adding 10,000 more messages for channel " + last_message.channel.name + "...")
						working_messages = self.bot.logs_from(self.get_channel(channel_list[channel]), before=last_message,
														  limit=10000)

					else:
						print("Finished parsing " + last_message.channel.name)
						finished_parsing = 0

				except discord.errors.Forbidden:
					print("Don't have acess to " + channel + "!")
					finished_parsing = 0

				except discord.errors.HTTPException:
					print("Something Broke Processing this: ", message.channel.name)
					finished_parsing = 0'''

			await self.bot.say(':dab:')

def setup(bot):
	bot.add_cog(BasicCog(bot))

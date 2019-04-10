import discord
from discord.ext import commands
import os


class ScrapingCog:
	def __init__(self, bot):
		self.bot = bot

	# # Grabs text from channels not in the bad channels list
	# @commands.command(name='chatGrab')
	# async def basic_chat_grab(self, channel_list):
	# 	if not os.path.exists('csvs'):
	# 		os.makedirs('csvs')
	#
	# 	f = open("csvs/chatlog.csv","a")
	# 	print("preparing channel")
	# 	for channel in channel_list:
	# 		working_messages = self.logs_from(self.get_channel(channel_list[channel]), limit=10_000)
	# 		finished_parsing = 1
	# 		last_message = discord.Message
	#
	# 		if channel in self.bad_channels:
	# 			finished_parsing = 0
	#
	# 		while finished_parsing:
	# 			try:
	# 				async for message in working_messages:
	# 					'''reactList = []
	# 					for i in message.reactions:
	# 						#windows has a problem with emoji
	# 						reactList.append(i.emoji)
	# 						reactList.append(i.count)'''
	#
	# 					#Message Format: id:::timestamp:::author:::content:::embeddedLinks:::attachments:::channel:::server
	# 					#curr_message = " {\"ID\": \"" + str(message.id) + "\", \"Year\": \"" + str(message.timestamp.year) + "\", \"Name\": \"" + message.author.name + "\", \"Message Content\": \"" + content + "\", \"Channel\": \"" + message.channel.name + "\", \"Reactions\": \"" + " ".join(str(v) for v in reactList) + "\"},\n"
	# 					#curr_message = (message.author.name + ":::" + message.content + "\n")
	#
	# 					if message.content != "" and message.author.name != "UB3R-B0T":
	# 						curr_message = str(message.id)+ "|" + str(message.timestamp) + "|" + message.author.id + "|" + message.author.name + "|" + message.content.replace ('\n','')  + "|" + str(message.embeds) + "|" + message.channel.name + "|" + message.server.name + "\n";
	# 						f.write(curr_message)
	#
	# 					last_message = message
	#
	# 				more_check = 0
	# 				async for i in self.logs_from(self.get_channel(channel_list[channel]), before=last_message, limit=10):
	# 					more_check += 1
	#
	# 				if more_check > 0:
	# 					print("Adding 10,000 more messages for channel " + last_message.channel.name + "...")
	# 					working_messages = self.logs_from(self.get_channel(channel_list[channel]), before=last_message, limit=10000)
	#
	# 				else:
	# 					print("Finished parsing " + last_message.channel.name)
	# 					finished_parsing = 0
	#
	# 			except discord.errors.Forbidden:
	# 				print("Don't have acess to " + channel + "!")
	# 				finished_parsing = 0
	#
	# 			except discord.errors.HTTPException:
	# 				print ("Something Broke Processing this: ", message.channel.name)
	# 				finished_parsing = 0
	#
	# 	print("All doneso!")
	# 	f.close()
	#
	# #Function that grabs all the text from general discussion (500,000+ messages, crashes with the regular function)
	# @commands.command(name='largeChatGrab')
	# async def large_chat_grab(self, channelName, channelList):
	#
	# 	if not os.path.exists('dictionaries'):
	# 		os.makedirs('dictionaries')
	#
	# 	print("Starting general grab...")
	# 	general_messages = self.logs_from(self.get_channel(channelList[channelName]), limit=100000)
	# 	f = open("dictionaries/generalList.txt","a")
	#
	# 	more_check = 1
	# 	last_message = discord.Message
	#
	# 	while more_check:
	# 		async for message in general_messages:
	# 			f.write(str(message.id) + "|" + str(message.timestamp) + "|" + message.author.id + "|" + message.author.name + "|" + message.content.replace ('\n','')  + "|" + str(message.embeds) + "|" + message.channel.name + "|" + message.server.name + "\n")
	# 			last_message = message
	#
	# 		more_check = 0
	# 		async for i in self.logs_from(self.get_channel(channelList["general_discussion"]), before=last_message, limit=10):
	# 			more_check += 1
	#
	# 		if more_check > 0:
	# 			print("Adding 100,000 more messages for channel...")
	# 			general_messages = self.logs_from(self.get_channel(channelList["general_discussion"]), before=last_message, limit=100_000)
	# 		else:
	# 			print("Finished parsing!")
	#
	# 	f.close()
	#
	# #Creates individual dictionary files out of the master list
	# @commands.command(name='mti')
	# async def master_to_individual(self):
	# 	dict_list = open("dictionaries/masterList.txt","r")
	#
	# 	for i in dict_list:
	# 		message_val = i.split(":::")
	# 		if len(message_val) == 2:
	# 			file_path = "dictionaries/" + message_val[0] + "Dictionary.txt"
	# 			f = open(file_path, "a")
	# 			f.write(message_val[1])
	# 			f.close()
	#
	# 	print("Finished!")

	#Creates user defined dictionary
	@commands.command(name='ci')
	async def create_individual(self, channel_list, username):
		file_path = "dictionaries/" + str(username) + "Dictionary.txt"
		f = open(file_path, "w")

		working_messages = self.bot.logs_from(self.bot.get_channel(self.bot.server_dict[channel_list]), limit=100000)
		finished_parsing = 1
		last_message = discord.Message

		async for message in working_messages:
			if message.author.name == username:
				f.write(message.content + "\n")


		# while finished_parsing:
		# 	try:
		# 		async for message in working_messages:
		# 			if message.author.name == username:
		# 				f.write(str(message.content.encode("utf-8")) + "\n")
		#
		# 		moreCheck = 0
		# 		async for i in self.logs_from(self.bot.get_channel(self.bot.server_dict[channel_list]), before=last_message, limit=10):
		# 			moreCheck += 1
		#
		# 		if moreCheck > 0:
		# 			print("Adding 10000 more messages for channel " + last_message.channel.name + "...")
		# 			working_messages = self.logs_from(self.bot.get_channel(self.bot.server_dict[channel_list]), before=last_message, limit=10000)
		# 		else:
		# 			print("Finished Parsing " + last_message.channel.name)
		# 			finished_parsing = 0
		#
		# 	except discord.errors.Forbidden:
		# 		print("Don't have acesss to " + channel_list + "!")
		# 		finished_parsing = 0
		#
		# 	except discord.errors.HTTPException:
		# 		print ("Something Broke Processing this: ", message.channel.name)
		# 		finished_parsing = 0
		#
		# 	except UnicodeEncodeError:
		# 		print("Ran into a unicode error")


def setup(bot):
	bot.add_cog(ScrapingCog(bot))

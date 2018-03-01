from discord.ext import commands
import basic, scraping, markov
import discord, os, aiohttp

bot = commands.Bot(command_prefix='wb', description="WoodyBot mk 0.420")

try:
	f = open('credentials.txt', 'r')
	login_info = f.read().split(':')
	f.close()

except IOError:
	userVal = input("Please enter a username: ")
	passVal = input("Please enter a password: ")
	login_info = [userVal,passVal]

workingSent = ""
channelList = {}

#Sets up a dict of servers and channels
#Format: { channelName:channel id}
@bot.event
async def on_ready():
	for server in bot.servers:
		for channel in server.channels:
			if channel.type == discord.ChannelType.text:
				channelList[channel.name] = channel.id

	print ("We're live!")

@bot.event
async def on_message(message):
	if message.author.name == "Stormagedon":
		await bot.add_reaction(message, "🐎")

	if (message.channel.name == "fa_inspo" and message.content != ""):
		if message.content.startswith("http") or message.content.startswith("www"):
			return
		else:
			await bot.delete_message(message)

	await bot.process_commands(message)


'''Basic Commands'''
@bot.command()
async def hallo():
	await bot.say("hallo")

#Downloads all the images from an input channel
@bot.command()
async def channelDownload(channelName: str):
	await basic.channelDownload(bot, channelName, channelList)

#Broken as of right now
'''
#Reads through a channel's messages and returns a string of the most reacted message
@bot.command()
async def statParse(channelName: str, limitVal: int):
	await basic.statParse(bot, channelName, limitVal)


@bot.command()
async def wordCount(keyword: str):
	await basic.wordCount(bot, keyword)
'''

'''Scraping functions'''
@bot.command()
async def basicChatGrab(channelList: dict):
	await scraping.basicChatGrab(bot, channelList)

@bot.command()
async def largeChatGrab(channelName: str, channelList: dict):
	await scraping.largeChatGrab(bot, channelName, channelList)

@bot.command()
async def individualDictionaryCreate():
	await scraping.masterToInidividual()

#Broken as of right now
'''
@bot.command()
async def addDictionary(*, username: str):
	await scraping.createIndividual(bot, channelList, username)
'''

'''Markov Functions'''
@bot.command()
async def markovSimulate(username: str):
	response = markov.startMarkove(username)
	await bot.say(response)




bot.run(login_info[0], login_info[1])
from discord.ext import commands
import discord
import basic
import scraping
import markov
import redditFunctions
import os
import aiohttp

bot = commands.Bot(command_prefix='wb', description="WoodyBot mk 0.420")

try:
	f = open('credentials.txt', 'r')
	login_info = f.read().split(':')
	f.close()

except IOError:
	userVal = input("Please enter a username: ")
	passVal = input("Please enter a password: ")
	login_info = [userVal, passVal]

workingSent = ""
channel_list = {}


# Sets up a dict of servers and channels
# Format: { channelName:channel id}
@bot.event
async def on_ready():
	for server in bot.servers:
		for channel in server.channels:
			if channel.type == discord.ChannelType.text:
				channel_list[channel.name] = channel.id

	print("We're live!")


# On reading a message, parses the input for commands
@bot.event
async def on_message(message):
	if message.author.name == "Stormagedon":
		await bot.add_reaction(message, "🐎")

	if message.channel.name == "fa_inspo" and message.content != "":
		if message.content.startswith("http") or message.content.startswith("www"):
			return
		else:
			await bot.delete_message(message)

	await bot.process_commands(message)


# [Basic Commands]
# Downloads all the images from an input channel
@bot.command()
async def imageDownload(channel_name: str):
	await basic.channel_download(bot, channel_name, channel_list)


@bot.command()
async def kooda():
	await bot.say("https://www.youtube.com/watch?v=yz7Cn3pHibo")


# [Scraping Functions]
# Downloads and formats chat not in the 'Bad Channels' array
@bot.command()
async def chatDownload():
	await scraping.basic_chat_grab(bot, channel_list)


# Downloads and formats chat from a specified channel
@bot.command()
async def large_chat_download(channel_name: str):
	await scraping.large_chat_grab(bot, channel_name, channel_list)


# Creates a text file containing the chats of a specific user
@bot.command()
async def create_user_dictionary():
	await scraping.masterToInidividual()


# [Markov Functions]
@bot.command()
async def mimic(*, username: str):
	response = markov.startMarkov(username)
	await bot.say(response)


# [Reddit-related Functions]
@bot.command(pass_context=True)
async def redditList(ctx, *args):
	top_list = await redditFunctions.list_top(ctx, args)
	await bot.say(top_list[0])
	
	workingDict = top_list[1]
	
	pChoice = await bot.wait_for_message(author=ctx.message.author)

	if pChoice.content.startswith("url"):
		pChoice = int(pChoice.content.split(" ")[1])
		if pChoice > 0 and pChoice < len(workingDict):
			choice = workingDict[pChoice-1]
			await bot.say(choice)
	

@bot.command(pass_context=True)
async def joined(ctx, *, member: discord.Member):
	await ctx.bot.say('{0} joined on {0.joined_at}'.format(member))




bot.run(login_info[0], login_info[1])
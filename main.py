import asyncio, aiohttp, os, random, discord
import scraping, markov
from markov import *

client = discord.Client(max_messages = 500)
f = open('credentials.txt', 'r')
login_info = f.read().split(':')
f.close()

workingSent = ""
channelList = {}
	
#Sets up a dict of servers and channels
#Format: { channelName:channel id}
@client.async_event
async def on_ready():
	for server in client.servers:
		for channel in server.channels:
			if channel.type == discord.ChannelType.text:
				channelList[channel.name] = channel.id

	print ("We're live!")
	await client.change_presence()

#Sets the bot to do certain behavior when it reads a message
@client.async_event
async def on_message(message):
	if message.content.lower().find('woodybot') != -1:
		await client.add_reaction(message, "👀")

		workingSent = message.content.split(" ")
		for i in workingSent:
			print (i)
		isMod = 0
		for i in message.author.roles:
			if 'Moderators' == i.name:
				isMod = 1

		#Me Privs
		if message.author.name == "WoodyAllen":
			if workingSent[1] == "Download":
				await channelDownload(workingSent[2])
			if workingSent[1] == "DisplayChan":
				for i in channelList:
						print (i + ": " + channelList[i])
			if workingSent[1] == "SnatchWeave":
				await snatchWeave(workingSent[2])
			if workingSent[1] == "WordCount":
				await wordCount(workingSent[2])
			if workingSent[1] == "GimmieWords":
				await start_parse()
			if workingSent[1] == "gg":
				await grab_gen()
			if workingSent[1] == "indidict":
				await dictToIndividual()


		#Mod Privs
		

		#Everyone Privs
		if message.author.name == "auden":
			await client.add_reaction(message, "🏳️‍🌈")

		if workingSent[1] == "ViewStats":
			limVal = 400
			if (len(workingSent) >= 4): limBal = workingSent[3]
			await statParse(workingSent[2], limVal)

		if workingSent[1][-5:].lower() == "speak":
			name = workingSent[1].split("speak")
			sentence = startMarkov(name[0])
			await client.send_message(message.channel, sentence)

	if (message.channel.name == "fa_inspo" and message.content != ""):
		if message.content.startswith("http") or message.content.startswith("www"):
			return
		else:
			await client.delete_message(message)

#Reads through a channel's messages and returns a string of the most reacted message
@client.async_event
async def statParse(channelName, limitVal):
	workingID = channelList[channelName]
	workingLog = client.logs_from(client.get_channel(workingID), limit=int(limitVal))
	mostReacted = discord.Message
	maxReacts = 0

	async for wMess in workingLog:
		if wMess.reactions != []:
			reactTotal = 0
			for react in wMess.reactions:
				reactTotal += react.count

			if reactTotal > maxReacts:
				maxReacts = reactTotal
				mostReacted = wMess

	finalString = "Most reactions is \"" + mostReacted.content + "\" from " + mostReacted.author.name + " with a total of "+ str(maxReacts) + " reactions"
	await client.send_message(mostReacted.channel, finalString )


#Downloads all the images from an input channel
@client.async_event
async def channelDownload(channelName):
	if channelName in channelList:
		tempWorkPath = "pictures/" + channelName
		if not os.path.exists(tempWorkPath):
			os.makedirs(tempWorkPath)
	else:
		print ("something wrong happened")
		return

	workingPath = os.path.join(os.getcwd(), tempWorkPath)

	imageCounter = 0;
	finalName = ""
	blicky = []

	
	totalLogs = client.logs_from(client.get_channel(channelList[channelName]), limit=10000)
	async for i in totalLogs:
		if i.attachments != []:
			if (i.attachments[0]['filename'] == 'image.png' or i.attachments[0]['filename'] == 'image.jpg'):						
				tempName = i.attachments[0]['filename'].split(".")
				finalName = tempName[0] + str(imageCounter) + "." + tempName[1]
				imageCounter += 1
			else:
				finalName = i.attachments[0]['filename']

			blicky.append([os.path.join(workingPath, finalName),i.attachments[0]['url']])

	for i in blicky:
		await download_file(i[0],i[1]);		
	
#Helper function for the channelDownload
def write_to_file(filename, content):
	print("writing to ", filename)
	f = open(filename, 'wb')
	f.write(content)
	f.close()

#Helper function for channelDownload
@client.async_event
async def download_file(filename, url):
	with aiohttp.ClientSession() as session:
		async with session.get(url) as melon:
			content = await melon.read()
			write_to_file(filename,content)

#Counts the amount of times keyword is said in a particular channel
@client.async_event
async def wordCount(keyword):
	govProp = {}
	print("Starting word count")
	for channelName in channelList:
		workingMessages = client.logs_from(client.get_channel(channelList[channelName]), limit=10000)
		print("Parsing ", channelName)
		finishedParsing = 1

		lastMessage = discord.Message
		if channelName == "general_discussion":
			finishedParsing = 0
			
		while (finishedParsing):
			try:
				async for message in workingMessages:
					lastMessage = message
					if message.content.lower().find(keyword) != -1:
						if message.author.name not in govProp:
							govProp[message.author.name] = 1
						else:
							govProp[message.author.name] = govProp[message.author.name] + 1


				moreCheck = 0
				async for i in client.logs_from(client.get_channel(channelList[channelName]), before=lastMessage, limit=10):
					moreCheck += 1

				if moreCheck > 0:
					print("Adding 10000 more messages for channel " + lastMessage.channel.name + "...")
					workingMessages = client.logs_from(client.get_channel(channelList[channelName]), before=lastMessage, limit=10000)
				else:
					print("Finished Parsing " + lastMessage.channel.name)
					finishedParsing = 0

			except discord.errors.Forbidden:
				print("Don't have acess to " + channelName + "!")
				finishedParsing = 0

	mostWord = ""
	mostVal = 0

	for i in govProp:
		if govProp[i] > mostVal:
			mostVal = govProp[i]
			mostWord = i


	print ("The word " + keyword + " has been said a total of " + str(mostVal) + " times by " + mostWord + " (excluding general)")

@client.async_event
async def start_parse():
	await scraping.simpleChatGrab(client, channelList)

@client.async_event
async def grab_gen():
	await scraping.grabGen(client, channelList)

@client.async_event
async def dictToIndividual():
	await scraping.masterToIndividual()


client.run(login_info[0], login_info[1])

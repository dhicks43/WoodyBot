
import discord
from markov import *

client = discord.Client(max_messages = 500)

f = open('credentials.txt', 'r')
login_info = f.read().split(':')
f.close()

workingSent = ""
channelList = {}

@client.async_event
async def on_ready():
	for server in client.servers:
		for channel in server.channels:
			if channel.type == discord.ChannelType.text:
				channelList[channel.name] = channel.id

	print ("We're live!")
	await client.change_presence()

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
				await serverToJson()
			if workingSent[1] == "gg":
				await grabGen()


		#Mod Privs
		

		#Everyone Privs
		if message.author.name == "auden":
			await client.add_reaction(message, "🏳️‍🌈")

		if workingSent[1] == "ViewStats":
			limVal = 400
			if (len(workingSent) >= 4): limBal = workingSent[3]
			await statParse(workingSent[2], limVal)

		if workingSent[1].lower() == "audenspeak":
			sentence = startMarkov()
			await client.send_message(message.channel, sentence)

		if workingSent[1].lower() == "metrospeak":
			sentence = startMarkovM()
			await client.send_message(message.channel, sentence)

		if workingSent[1].lower() == "cazspeak":
			sentence = startMarkovC()
			await client.send_message(message.channel, sentence)

		if workingSent[1].lower() == "b4cspeak":
			sentence = startMarkovB4C()
			await client.send_message(message.channel, sentence)

		if workingSent[1].lower() == "turdspeak":
			sentence = startMarkovT()
			await client.send_message(message.channel, sentence)

		if workingSent[1].lower() == "kylespeak":
			sentence = startMarkovK()
			await client.send_message(message.channel, sentence)


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



@client.async_event
async def channelDownload():
	if not os.path.exists('pictures'):
		os.makedirs('pictures')

	workingPath = os.path.join(os.getcwd(), 'pictures')

	imageCounter = 0;
	finalName = "";

	blicky = []

	totalLogs = client.logs_from(client.get_channel("353132552707506178"), limit=10000)
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

def write_to_file(filename, content):
	print("writing to ", filename)
	f = open(filename, 'wb')
	f.write(content)
	f.close()

@client.async_event
async def download_file(filename, url):
	with aiohttp.ClientSession() as session:
		async with session.get(url) as melon:
			content = await melon.read()
			write_to_file(filename,content)

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
async def snatchWeave(username):
	filename = username + "Dictionary.txt"
	f = open(filename, 'a')

	for channelName in channelList:
		workingMessages = client.logs_from(client.get_channel(channelList[channelName]), limit=10000)
		finishedParsing = 1
		lastMessage = discord.Message
		if channelName == "general_discussion" or channelName == "music_bot":
			finishedParsing = 0
			
		while (finishedParsing):
			try:
				async for message in workingMessages:
					lastMessage = message
					if message.author.name == "Kylirr":
						f.write(message.content+"\n")

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




	print("Weave has been snatched!")
	f.close()


@client.async_event
async def serverToJson():
	f = open("banana.json","a")

	for channel in channelList:
		workingMessages = client.logs_from(client.get_channel(channelList[channel]), limit=10000)
		finishedParsing = 1
		lastMessage = discord.Message
		if channel == "general_discussion":
			finishedParsing = 0

		while (finishedParsing):
			try:
				async for message in workingMessages:
					reactList = []
					for i in message.reactions:
						
						reactList.append(i.emoji)
						reactList.append(i.count)

					currMessage = { 
						"ID": message.id,
						"Author" : message.author.name, 
						"Content": message.content, 
						"Embeds": message.embeds, 
						"Attachments": message.attachments, 
						"Channel": message.channel.name, 
						"Reactions": reactList
						}

					f.write(str(currMessage) + "\n")

				moreCheck = 0
				async for i in client.logs_from(client.get_channel(channelList[channel]), before=lastMessage, limit=10):
					moreCheck += 1

				if moreCheck > 0:
					print("Adding 10000 more messages for channel " + lastMessage.channel.name + "...")
					workingMessages = client.logs_from(client.get_channel(channelList[channel]), before=lastMessage, limit=10000)
				else:
					print("Finished Parsing " + lastMessage.channel.name)
					finishedParsing = 0

			except discord.errors.Forbidden:
				print("Don't have acess to " + channel + "!")
				finishedParsing = 0

			except discord.errors.HTTPException:
				print ("Something Broke Processing this: ", message.channel.name)
				finishedParsing = 0

@client.async_event
async def grabGen():
	print("Starting general grab...")
	generalMessages = client.logs_from(client.get_channel(channelList["general_discussion"]), limit=100000)
	f = open("THISISGENERAL.txt","a")

	moreCheck = 1
	lastMessage = discord.Message

	while(moreCheck):
		async for message in generalMessages:
			f.write(message.author.name + "::" + message.content + "\n")
			lastMessage = message
				
		moreCheck = 0
		async for i in client.logs_from(client.get_channel(channelList["general_discussion"]), before=lastMessage, limit=10):
			moreCheck += 1

		if moreCheck > 0:
			print("Adding 100,000 more messages for channel...")
			generalMessages = client.logs_from(client.get_channel(channelList["general_discussion"]), before=lastMessage, limit=100000)
		else:
			print("Finished parsing!")

	f.close()






client.run(login_info[0], login_info[1])

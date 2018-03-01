import os, discord, aiohttp

#Downloads all the images in a selected channel
async def channelDownload(bot: discord.ext.commands.Bot, channelName: str, channelList: dict):
	if channelName in channelList:
		tempWorkPath = "pictures/" + channelName
		if not os.path.exists(tempWorkPath):
			os.makedirs(tempWorkPath)
	else:
		print ("Channel not found!")
		return

	workingPath = os.path.join(os.getcwd(), tempWorkPath)

	imageCounter = 0;
	finalName = ""
	blicky = []

	
	totalLogs = bot.logs_from(bot.get_channel(channelList[channelName]), limit=10000)
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
async def download_file(filename, url):
	with aiohttp.ClientSession() as session:
		async with session.get(url) as melon:
			content = await melon.read()
			write_to_file(filename,content)

#Parses a channel the most used emoji, currently broken
'''
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
'''

#Counts the amount of times keyword is said in a particular channel
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
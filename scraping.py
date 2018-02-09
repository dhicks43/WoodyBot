import discord, os

bad_channels = {"general_discussion","music_bot"}
#Grabs text from channels not named general_discussion and music_bot
async def simpleChatGrab(client, channelList):
	
	if not os.path.exists('dictionaries'):
		os.makedirs('dictionaries')

	f = open("dictionaries/masterList.txt","a")

	for channel in channelList:
		workingMessages = client.logs_from(client.get_channel(channelList[channel]), limit=10000)
		finishedParsing = 1
		lastMessage = discord.Message
		if channel in bad_channels:
			finishedParsing = 0

		while (finishedParsing):
			try:
				async for message in workingMessages:
					'''reactList = []
					for i in message.reactions:
						#windows has a problem with emoji
						reactList.append(i.emoji.id)
						reactList.append(i.count)
						content = message.content

					format = { [id, timestamp, author, content, embeddedLinks, attachments, channel, reactions[] ]}'''
					#currMessage = message.id + "," + str(message.timestamp.year) + "," + message.author.name + "," + message.content + "," + " ".join(str(v) for v in message.embeds) + "," + " ".join(str(v) for v in message.attachments) + "," + message.channel.name + "," + " ".join(str(v) for v in reactList) + "\n"
					
					currMessage = (message.author.name + ":::" + message.content + "\n")
					f.write(currMessage)

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

	f.close()

#Function that grabs all the text from general discussion (500,000+ messages, crashes with the regular function)
async def grabGen(client, channelList):

	if not os.path.exists('dictionaries'):
		os.makedirs('dictionaries')

	print("Starting general grab...")
	generalMessages = client.logs_from(client.get_channel(channelList["general_discussion"]), limit=100000)
	f = open("dictionaries/generalList.txt","a")

	moreCheck = 1
	lastMessage = discord.Message

	while(moreCheck):
		async for message in generalMessages:
			f.write(message.author.name + ":::" + message.content + "\n")
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

#Creates individual dictionary files out of the master list
async def masterToIndividual():
	dictlist = open("dictionaries/masterList.txt","r")
	
	for i in dictlist:
		messageVal = i.split(":::")
		if(len(messageVal) == 2):
			filepath = "dictionaries/" + messageVal[0] + "Dictionary.txt"
			f = open(filepath, "a")
			f.write(messageVal[1])
			f.close()

	print("Finished!")


async def createIndividual(client, channelList, username):
	print(username)
	filepath = "dictionaries/" + username + "Dictionary.txt"
	f = open(filepath,"a")

	for channel in channelList:
		workingMessages = client.logs_from(client.get_channel(channelList[channel]), limit=10000)
		finishedParsing = 1
		lastMessage = discord.Message
		if channel != "loef":
			finishedParsing = 0

		while (finishedParsing):
			try:
				async for message in workingMessages:
					if message.author.name == username:
						f.write(message.content + "\n")

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
		

 






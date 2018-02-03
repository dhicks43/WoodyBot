import asyncio, aiohttp, os, random, discord

def startMarkov(user):
	dictname = "dictionaries/" +user + "Dictionary.txt"
	
	try:
		f = open(dictname, "r")

	except IOError:
		return dictname + " doesn't exist!"

	wordList = {}

	for line in f:
		curDict = line.split(" ")

		while (len(curDict) > 1):
			if (curDict[0] not in wordList):
				wordList[curDict[0]] = [ curDict[1] ]
			else:
				wordList[curDict[0]].append(curDict[1])

			curDict.pop(0)


	word = random.choice(list(wordList.keys()))
	sentence = []
	sentence.append(word)
	while(word in wordList.keys()):
		word = random.choice(wordList[word])
		sentence.append(word)

	finalsentence = " ".join(sentence)

	return finalsentence


'''
Legacy Functions

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
	'''

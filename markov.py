import asyncio, aiohttp, os, random, discord

def startMarkov(user):
	dictname = user + "Dictionary.txt"
	
	try:
		f = open(dictname, "r")

	except IOError:
		print(dictname + " doesn't exist!")
		return "empty"

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

def startMarkovM():
	f = open("metroDictionary.txt", "r")
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

def startMarkovC():
	f = open("cazDictionary.txt", "r")
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

def startMarkovB4C():
	f = open("b4cDictionary.txt", "r")
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

def startMarkovT():
	f = open("turdpunDictionary.txt", "r")
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

def startMarkovK():
	f = open("kyleDictionary.txt", "r")
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


def gibbieAuden():
	f = open("newKyle.txt","a")
	g = open("THISISGENERAL.txt", "r")

	for line in g:
		bing = line.split("::")
		if(bing[0] == "Kylirr"):
			f.write(bing[1])


'''
Testing or broken functions
@client.async_event
async def snatchWeave(username):


def genMarkovText(textfile){
	writeTo = open("audent.txt","r")
	readFrom = open(textFile, "w")



}'''

#format = { [id, timestamp, author, content, embeddedLinks, attachments, channel, reactions[] ]}






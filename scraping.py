import discord

async def serverToJson(client, channelList):
	f = open("banana.txt","a")

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

					currMessage = str("ID"+ message.id +
					 					"Timestamp"+ message.timestamp.year +
					 					"Author" + message.author.name +
					 					"Content" + message.content +  
					 					"Embeds" + message.embeds +  
					 					"Attachments" + message.attachments +  
					 					"Channel" + message.channel.name +  
					 					"Reactions" + str(reactList) + "\n")
					

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
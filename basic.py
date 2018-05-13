import os
import discord.ext
import aiohttp


# Downloads all the images in a selected channel
async def channel_download(bot: discord.ext.commands.Bot, channel_name: str, channel_list: dict):
	if channel_name in channel_list:
		temp_work_path = "pictures/" + channel_name
		if not os.path.exists(temp_work_path):
			os.makedirs(temp_work_path)

	else:
		print("Channel not found!")
		return

	working_path = os.path.join(os.getcwd(), temp_work_path)

	image_counter = 0
	filepath_url_combo = []
	
	total_logs = bot.logs_from(bot.get_channel(channel_list[channel_name]), limit=10000)

	async for _ in total_logs:
		if len(_.attachments) > 0:
			if _.attachments[0]['filename'] == 'image.png' or _.attachments[0]['filename'] == 'image.jpg':
				temp_name = _.attachments[0]['filename'].split(".")
				final_name = temp_name[0] + str(image_counter) + "." + temp_name[1]
				image_counter += 1

			else:
				final_name = _.attachments[0]['filename']

			filepath_url_combo.append([os.path.join(working_path, final_name), _.attachments[0]['url']])

	for _ in filepath_url_combo:
		await download_file(_[0], _[1])


# Helper function for the channelDownload
def write_to_file(filename, content):
	print("writing to ", filename)
	f = open(filename, 'wb')
	f.write(content)
	f.close()


# Helper function for channelDownload
async def download_file(filename, url):
	with aiohttp.ClientSession() as session:
		async with session.get(url) as grabbed_url:
			content = await grabbed_url.read()
			write_to_file(filename, content)


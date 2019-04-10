import os
import aiohttp
from discord.ext import commands


# Downloads all the images in a selected channel
@commands.command(name="channelDownload")
async def channel_download(self, channel_name, user_name=None):
    if channel_name in self.bot.server_dict[self.bot]:
        temp_work_path = "pictures/" + channel_name
        if user_name:
            temp_work_path += "_" + user_name

        if not os.path.exists(temp_work_path):
            os.makedirs(temp_work_path)

    else:
        print("Channel not found!")
        return

    working_path = os.path.join(os.getcwd(), temp_work_path)

    image_counter = 0
    filepath_url_combo = []

    total_logs = self.bot.logs_from(self.bot.get_channel(self.bot.server_dict[channel_name]), limit=10000)

    async for _ in total_logs:
        if len(_.attachments) > 0:
            if user_name:
                if _.author.name != user_name:
                    continue

            if _.attachments[0]['filename'] == 'image.png' or _.attachments[0]['filename'] == 'image.jpg':
                temp_name = _.attachments[0]['filename'].split(".")
                final_name = temp_name[0] + str(image_counter) + "." + temp_name[1]
                image_counter += 1

            else:
                final_name = _.attachments[0]['filename']

            filepath_url_combo.append([os.path.join(working_path, final_name), _.attachments[0]['url']])

    for _ in filepath_url_combo:
        await self.download_file(_[0], _[1])

	# Helper function for the channelDownload
	async def write_to_file(self, filename, content):
		print("writing to ", filename)
		f = open(filename, 'wb')
		f.write(content)
		f.close()

	async def download_file(self, filename, url):
		with aiohttp.ClientSession() as session:
			async with session.get(url) as grabbed_url:
				content = await grabbed_url.read()
				await self.write_to_file(filename, content)
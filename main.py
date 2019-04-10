import discord
import logging
from pymongo import MongoClient
from discord.ext import commands


class WoodyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='wb', description="WoodyBot mk 0.525")
        self.server_dict = {}
        self.ping_dict = {}

        self.bad_channels = []

        self.dLog = logging.getLogger('discord')

        self.mongo_database = MongoClient().woodybot_db

    async def on_ready(self):
        # Sets up a dict of servers and channels
        # Format: { channelName:channel id}
        self.bad_channels = ["loef"]

        self.dLog.setLevel(logging.INFO)
        hand = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        hand.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.dLog.addHandler(hand)

        for server in self.servers:
            for channel in server.channels:
                if channel.type == discord.ChannelType.text:
                    bot.server_dict[channel.name] = channel.id

        print("We're live!")

    # On reading a message, parses the input for commands
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.name == "Stormagedon":
            await self.add_reaction(message, "🐎")


with open('credentials.txt', 'r') as f:
    login_info = f.read().split(':')

bot = WoodyBot()

installed_cogs = {"cogs.basic", "cogs.markov", "cogs.reddit", "cogs.scraping"}
for cog in installed_cogs:
    try:
        bot.load_extension(cog)

    except Exception as e:
        print(f"Cog {cog} failed to load")

if len(login_info) == 2:
    bot.run(login_info[0], login_info[1], bot=True, reconnect=True)

else:
    bot.run(login_info[0], bot=True, reconnect=True)



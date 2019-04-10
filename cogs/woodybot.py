import discord
import logging
from discord.ext import commands


class WoodyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='wb', description="WoodyBot mk 0.525")
        self.server_dict = {}
        self.threads_dict = {}

        self.dLog = logging.getLogger('discord')

    async def on_ready(self):
        self.dLog.setLevel(logging.INFO)
        hand = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        hand.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.dLog.addHandler(hand)

        # Sets up a dict of servers and channels
        # Format: { channelName:channel id}
        for server in self.servers:
            self.server_dict[server.name] = [{channel.name: channel} for channel in server.channels]

        for server in self.server_dict:
            print(server)
        print("We're live!")

    # On reading a message, parses the input for commands
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.name == "Stormagedon":
            await self.add_reaction(message, "🐎")

        await self.process_commands(message)

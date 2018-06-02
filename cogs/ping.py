from discord.ext import commands
from copy import copy


class PingCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='callPing', aliases=['call'])
    async def call_ping(self, ctx, *args):
        ping_message_copy = copy(self.ping_dict[ctx])
        return_message = ping_message_copy.pop()

        for _ in ping_message_copy:
            return_message += " " + str("<@" + str(_) + ">")

        await self.say(return_message)

    @commands.command(name='makePing', aliases=['mPing'])
    async def make_ping(self, ctx, *args):
        mention_id_list = [_ for _ in ctx.message.raw_mentions]

        await self.say("Please list a name for the command")
        ping_name = await self.wait_for_message(author=ctx.message.author)
        ping_name = ping_name.content

        await self.say("Please name the alert message you the users to be pinged with")
        ping_message = await self.wait_for_message(author=ctx.message.author)
        ping_message = ping_message.content

        mention_id_list.append(ping_message)
        self.ping_dict[ping_name] = mention_id_list

        await self.say("Command \"{}\" created!".format(ping_name))


def setup(bot):
    bot.add_cog(PingCog(bot))

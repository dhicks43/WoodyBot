import requests
from discord.ext import commands


class RedditCog:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='listtop', aliases=['redditlist'], pass_context=True)
	async def reddit_list(self, ctx, *args):
		top_list = await self.list_top(ctx, args)
		await self.bot.say(top_list[0])

		working_dict = top_list[1]

		p_choice = await self.bot.wait_for_message(author=ctx.message.author)

		if p_choice.content.startswith("url"):
			p_choice = int(p_choice.content.split(" ")[1])
			if p_choice > 0 and p_choice < len(working_dict) + 1:
				choice = working_dict[p_choice - 1]
				await self.bot.say(choice)

	async def list_top(self, ctx, args):
		"""
		Is given a list of arguments and returns a list of URL links to the related subreddit

		:param self: the current Discord client context
		:param 2 args: arg[0] = limit, arg[1] = subreddit: str
		:param 1 args: arg[0] = limit
		:param 0 args: defaultURL is used (Frugal Male Fashion subreddit, limit of 10)
		:return: list of the top limit number of reddit posts in the last 24 hours in the specified subreddit
		"""

		subreddit = "frugalmalefashion"
		limit = 10

		if len(args) == 2:
			limit = args[0]
			subreddit = args[1]

		if len(args) == 1 and type(args) == int:
			limit = args[0]

		if int(limit) > 25:
			limit = str(25)

		working_url = "https://www.reddit.com/r/" + subreddit + "/top/.json?raw_json=1&sort=top&t=day&limit=" + str(limit)

		r = requests.get(working_url, headers={'User-agent': self.bot.description})
		data = r.json()
		data_array = {}
		final_output = ""

		await self.bot.say("Printing the top " + str(limit) + " threads in the last 24 hours in subreddit " + subreddit + ":")

		for i, child in enumerate(data['data']['children']):
			final_output += str(i+1) + ". " + child['data']['title'] + '\n'
			data_array[i] = child['data']['url']

		response_list = [final_output, data_array]
		return response_list


def setup(bot):
	bot.add_cog(RedditCog(bot))

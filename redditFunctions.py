import requests

'''
subreddit = "frugalmalefashion"
limit = 10
defaultURL = "https://www.reddit.com/r/frugalmalefashion/top/.json?raw_json=1&sort=top&t=day&limit=10"
'''


async def list_top(ctx, args):
	"""
	Is given a list of arguments and returns a list of URL links to the related subreddit

	:param ctx: the current Discord client context
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
	
	r = requests.get(working_url, headers={'User-agent': 'woodybot 0.525'})
	data = r.json()
	data_array = {}
	final_output = ""

	await ctx.bot.say("Printing the top " + str(limit) + " threads in the last 24 hours in subreddit " + subreddit + ":")
	
	for i, child in enumerate(data['data']['children']):
		final_output += str(i+1) + ". " + child['data']['title'] + '\n'
		data_array[i] = child['data']['url']

	response_list = [final_output, data_array]
	return response_list

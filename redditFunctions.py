import requests

'''
subreddit = "frugalmalefashion"
limit = 10
defaultURL = "https://www.reddit.com/r/frugalmalefashion/top/.json?raw_json=1&sort=top&t=day&limit=10"
'''

#argument list comes in as 0, 1, or 2
#If arg list length == 2, arg[0] = limit: int, arg[1] = subreddit: str
#if arg list length == 1, arg[0] = limit: int
#if arg list length == 0, defaultURL is used (Frugal Male Fashion, limit of 10)
async def fmfList(ctx, args):
	subreddit = "frugalmalefashion"
	limit = 10

	print(len(args))

	if len(args) == 2:
		limit = args[0]
		subreddit = args[1]

	if len(args) == 1:
		limit = args[0]

	workingURL = "https://www.reddit.com/r/" + subreddit + "/top/.json?raw_json=1&sort=top&t=day&limit="+ str(limit)
	
	r = requests.get(workingURL, headers = {'User-agent': 'woodybot 0.420'})
	data = r.json()
	dataArray = {}
	finalOutput = ""

	await ctx.bot.say("Printing the top " + limit + " threads in the last 24 hours in subreddit... " + subreddit)
	for i, child in enumerate(data['data']['children']):
		finalOutput += str(i+1) + ". " + child['data']['title'] + '\n'
		dataArray[i+1] = child['data']['url']

	responseList = [finalOutput, dataArray]
	return responseList



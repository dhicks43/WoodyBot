import cogs.woodybot as wb

with open('credentials.txt', 'r') as f:
    login_info = f.read().split(':')

bot = wb.WoodyBot()

installed_cogs = {"cogs.basic", "cogs.markov", "cogs.ping", "cogs.reddit", "cogs.scraping", "cogs.google"}
for cog in installed_cogs:
    try:
        bot.load_extension(cog)

    except Exception as e:
        print(f"Cog {cog} failed to load")

if len(login_info) == 2:
    bot.run(login_info[0], login_info[1], bot=True, reconnect=True)

else:
    bot.run(login_info[0], bot=True, reconnect=True)



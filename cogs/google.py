from googleapiclient.discovery import build
from discord.ext import commands


class GoogleCog:
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "AIzaSyB19K0qJS0TX7Yz2jBAOklL6GQEY6XmW5M"
        self.cse_id = "000598415578304483939:nc_b-_qqwxm"

    @commands.command(name="gsearch", aliases=['g', 'gg', 'google'], pass_context=True)
    async def google_search(self, ctx, *search_term: str):
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=search_term, cx=self.cse_id, num=10).execute()

        await self.bot.say(res['items'][0]['link'])



def setup(bot):
    bot.add_cog(GoogleCog(bot))

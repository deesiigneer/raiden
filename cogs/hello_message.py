from aiohttp import web
from nextcord.ext import commands, tasks
from nextcord.ext.commands.bot import Bot
from os import environ

app = web.Application()
routes = web.RouteTableDef()


class Webserver(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.web_server.start()

        @routes.get('/')
        async def welcome(request):
            return web.Response(text="Hello, world")

        self.webserver_port = int(environ.get('PORT', 8000))
        app.add_routes(routes)

    @tasks.loop()
    async def web_server(self):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, port=self.webserver_port)
        await site.start()

    @web_server.before_loop
    async def web_server_before_loop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Webserver(bot))

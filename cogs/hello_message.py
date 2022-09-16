from aiohttp import web
from nextcord import Color
from nextcord.ext import commands, tasks
from nextcord.ext.commands.bot import Bot
from os import environ
from pyspapi import SPAPI
from json import loads, load

app = web.Application()
routes = web.RouteTableDef()

api = SPAPI(card_id=environ.get('SP_CARD_ID', None),
            token=environ.get('SP_TOKEN', None))


class Webserver(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.web_server.start()

        @routes.get('/')
        async def welcome(request):
            return web.Response(text="Hello, world")

        @routes.post('/webhook/')
        async def dblwebhook(request):
            print('Received Webhook...')
            request_data = await request.read()
            header = request.headers.get('X-Body-Hash')
            verified = api.webhook_verify(data=request_data, header=header)
            if verified:
                payment = request_data.decode('utf-8').replace("'", '"')
                payment = loads(payment)
                webhook_data = str(payment['data'])
                webhook_data = webhook_data.split("-")
                channel_id = webhook_data[0]
                channel = bot.get_channel(int(channel_id))
                message_id = webhook_data[1]
                message = await channel.fetch_message(int(message_id))
                await message.add_reaction('✅')
            else:
                return 'Integrity of request compromised...', 401
            return 200

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

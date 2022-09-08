import nextcord
from nextcord.ext.commands.bot import Bot
from nextcord.embeds import Embed
from nextcord.ext import commands
from nextcord import Colour, Interaction, slash_command
from nextcord.user import ClientUser
from os import environ
from pyspapi import SPAPI

api = SPAPI(card_id=environ.get('SP_CARD_ID', None), token=environ.get('SP_TOKEN', None))

guilds = [850091193190973472]


class GeneralCommands(commands.Cog):

    def __init__(self: ClientUser, client: Bot):
        self.bot = client

    @slash_command(name='ping', description='Проверяет задежку бота', guild_ids=guilds)
    async def ping(self, interaction: Interaction):
        embed = Embed(title="Ping-pong",
                      description=f"Задержка примерно {round(self.bot.latency * 1000)}ms.",
                      color=Colour.from_rgb(47, 49, 54))
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @slash_command(name='help', description='Помощь по боту', guild_ids=guilds)
    async def help(self, interaction: Interaction):
        await interaction.response.send_message('in dev', ephemeral=True)

    @slash_command(name='check', description='Проверяет наличие проходки на СПм', guild_ids=guilds)
    async def check(self, interaction: Interaction, user: nextcord.User = nextcord.SlashOption(
                                  name='user',
                                  description='Пользователь в Discord',
                                  required=False
                              )):
        if user is not None:
            await interaction.response.send_message(f'{api.get_user(user.id)}', ephemeral=True)
        else:
            await interaction.response.send_message(f'{api.get_user(interaction.user.id)}', ephemeral=True)


def setup(bot):
    bot.add_cog(GeneralCommands(bot))

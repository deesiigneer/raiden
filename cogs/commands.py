import json

from nextcord.ext.commands.bot import Bot
from nextcord import ButtonStyle, Button, Interaction, Embed, Colour, slash_command, SlashOption, User
from nextcord.ext import commands
from nextcord.ui import View, Select, Modal, Button, button, TextInput
from nextcord.user import ClientUser
from os import environ
from sys import exc_info
from pyspapi import API

api = API(card_id=environ.get('SP_CARD_ID', None), token=environ.get('SP_TOKEN', None))

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
    async def check(self, interaction: Interaction, user: User = SlashOption(
        name='user',
        description='Пользователь в Discord',
        required=False
    )):
        try:
            if user is not None:
                spuser = await api.get_user(user.id)
            else:
                spuser = await api.get_user(interaction.user.id)
                user = interaction.user
            await interaction.response.send_message(f'У `{spuser}`({user.mention}) есть проходка на СПм', ephemeral=True)
        except Exception as e:
            print(e, f'\nat line {exc_info()[2].tb_lineno}')
            if interaction.response.is_done() is False:
                await interaction.response.send_message(f"[{exc_info()[2].tb_lineno}]Error: {e}",
                                                        ephemeral=True)
            elif interaction.response.is_done() is True:
                await interaction.followup.send(f"[{exc_info()[2].tb_lineno}]Error: {e}",
                                                ephemeral=True)

    @slash_command(name='donate', description='Проверка оплаты и одновременно пожертвования)', guild_ids=guilds)
    async def donate(self, interaction: Interaction, amount: int = SlashOption(
        name='amount',
        description='Кол-во аров для пожертвования',
        required=True
    )):
        try:
            if amount <= 0:
                await interaction.response.send_message(f"Сумма не должна быть меньше 0, указанная сумма = {amount}",
                                                        ephemeral=True)
            else:
                embed = Embed(title='Donate',
                              description='Если у этого сообщения, появится реакция от бота, значит оплата прошла успешно!')
                message = await interaction.channel.send(embed=embed)
                url = await api.payment(amount,
                                  redirect_url='https://spworlds.ru/',
                                  webhook_url=f'{environ.get("WEBHOOK_URL", None)}',
                                  data=f'{interaction.channel_id}-{message.id}')
                embed.set_footer(text='Для оплаты, нажмите кнопку ниже.')
                await message.edit(embed=embed, view=DonateButton(url=url['url']))
        except Exception as e:
            print(e, f'\nat line {exc_info()[2].tb_lineno}')
            if interaction.response.is_done() is False:
                await interaction.response.send_message(f"[{exc_info()[2].tb_lineno}]Error: {e}",
                                                        ephemeral=True)
            elif interaction.response.is_done() is True:
                await interaction.followup.send(f"[{exc_info()[2].tb_lineno}]Error: {e}",
                                                ephemeral=True)


class DonateButton(View):
    def __init__(self, url=None):
        super().__init__(timeout=None)
        self.url = url
        try:
            if self.url is not None:
                self.add_item(
                    Button(style=ButtonStyle.link,
                           label='Перейти на сайт для оплаты',
                           url=f'{self.url}'))
            else:
                url = 'https://spworlds.ru/'
                self.add_item(
                    Button(style=ButtonStyle.link,
                           label='Перейти на сайт для оплаты',
                           url=f'{url}',
                           disabled=True))
        except Exception as e:
            print(e, f'\nat line {exc_info()[2].tb_lineno}')


def setup(bot):
    bot.add_cog(GeneralCommands(bot))

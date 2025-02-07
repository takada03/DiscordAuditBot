import disnake
from disnake.ext import commands
from disnake.ui import Button, View


TOKEN = 'YOURBOTTOKEN'


intents = disnake.Intents.default()
intents.messages = True
intents.members = True
bot = commands.InteractionBot(intents=intents)
ALLOWED_CHANNEL_ID = 123456789

user_data = {}


@bot.event
async def on_ready():
    print(f'Бот {bot.user} готов к работе!')

def is_allowed_channel(interaction: disnake.Interaction):
    return interaction.channel.id == ALLOWED_CHANNEL_ID



@bot.slash_command(description="Принять нового сотрудника.")
async def принятие(inter: disnake.ApplicationCommandInteraction, пользователь: disnake.Member, ранг: int,
                   причина: str):
    if not is_allowed_channel(inter):
        return await inter.response.send_message("Эта команда доступна только в определенном канале.", ephemeral=True)

    user_id = пользователь.id
    display_name = пользователь.display_name
    inter_user_id = inter.user.id
    inter_display_name = inter.user.display_name

    user_data[user_id] = {'id': user_id, 'ранг': ранг, 'статус': 'Принят'}

    embed = disnake.Embed(title="Отчет о приеме сотрудника",
                          )
    embed.add_field(name=f"> `Причина принятия:`{причина} ", value=f"\u200b", inline=False)
    embed.add_field(name=f"> `Принят на {ранг} ранг`", value=f"\u200b", inline=False)
    embed.add_field(name="Принят(a):", value=f"<@{user_id}>", inline=True)
    embed.add_field(name="Имя Фамилия:", value=f"{display_name}", inline=True)
    embed.add_field(name="Discord ID:", value=f"{user_id}", inline=True)
    embed.add_field(name="Принимает:", value=f"{inter.user.mention}", inline=True)
    embed.add_field(name="Имя Фамилия:", value=f"{inter_display_name}", inline=True)
    embed.add_field(name="Discord ID:", value=f"{inter_user_id}", inline=True)
    embed.add_field(name="Дата:", value=f"{disnake.utils.format_dt(disnake.utils.utcnow(), style='F')}", inline=False)
    await inter.response.send_message(embed=embed)



@bot.slash_command(description="Повысить сотрудника.")
async def повышение(inter: disnake.ApplicationCommandInteraction, пользователь: disnake.Member, с_ранга: int,
                    на_ранг: int, причина: str):
    if not is_allowed_channel(inter):
        return await inter.response.send_message("Эта команда доступна только в определенном канале.", ephemeral=True)

    user_id = пользователь.id
    display_name = пользователь.display_name

    embed = disnake.Embed(title="Отчет о повышении сотрудника", color=disnake.Color.light_gray())
    embed.add_field(name=f"> `Причина повышения:` {причина}", value="\u200b", inline=True)
    embed.add_field(name="> Повышен(а) с ранга на ранг:", value=f"`{с_ранга} ➝ {на_ранг}`", inline=False)

    embed.add_field(name="Повышен(а):", value=f"<@{user_id}>", inline=True)
    embed.add_field(name="Имя Фамилия:", value=f"{display_name}", inline=True)
    embed.add_field(name="Discord ID:", value=f"{user_id}", inline=True)

    embed.add_field(name="Повышает:", value=f"{inter.user.mention}", inline=True)
    embed.add_field(name="Имя Фамилия:", value=f"{inter.user.display_name}", inline=True)
    embed.add_field(name="Discord ID:", value=f"{inter.user.id}", inline=True)

    embed.set_footer(text=f"Дата: {disnake.utils.utcnow().strftime('%d.%m.%Y %H:%M')}")

    await inter.response.send_message(embed=embed)



@bot.slash_command(description="Уволить сотрудника.")
async def увольнение(inter: disnake.ApplicationCommandInteraction, пользователь: disnake.Member,
                     причина: str, с_ранга: int):
    if not is_allowed_channel(inter):
        return await inter.response.send_message("Эта команда доступна только в определенном канале.", ephemeral=True)

    user_id = пользователь.id
    display_name = пользователь.display_name

    embed = disnake.Embed(title="Отчет об увольнении сотрудника", color=disnake.Color.light_gray())
    embed.add_field(name=f"> `Причина увольнения:` {причина}", value=f"\u200b", inline=False)
    embed.add_field(name=f"> Уволен(a) с {с_ранга} ранга", value=f"\u200b", inline=False)
    embed.add_field(name="Уволен(a):", value=f"<@{user_id}>", inline=True)
    embed.add_field(name="Имя Фамилия:", value=f"{display_name}", inline=True)
    embed.add_field(name="Discord ID:", value=f"{user_id}", inline=True)
    embed.add_field(name="Уволил(а):", value=f"{inter.user.mention}", inline=True)
    embed.add_field(name="Имя Фамилия:", value=f"{inter.user.display_name}", inline=True)
    embed.add_field(name="Discord ID:", value=f"{inter.user.id}", inline=True)
    embed.set_footer(text=f"Дата: {disnake.utils.utcnow().strftime('%d.%m.%Y %H:%M')}")


    button = Button(label="Кикнуть", style=disnake.ButtonStyle.danger)

    async def on_kick_button_click(interaction: disnake.Interaction):

        if interaction.user.id != inter.user.id:
            await interaction.response.send_message("Вы не можете использовать эту кнопку.", ephemeral=True)
            return


        if not interaction.guild.me.guild_permissions.kick_members:
            await interaction.response.send_message("У меня нет прав для кика участников.", ephemeral=True)
            return


        try:
            await пользователь.kick(reason=f"Уволен(a) с причиной: {причина}")

            await interaction.response.edit_message(content="Пользователь был уволен и кикнут.", embed=embed,
                                                    components=[])
        except disnake.errors.Forbidden:
            await interaction.response.send_message("У меня нет прав на кик этого пользователя.", ephemeral=True)

    button.callback = on_kick_button_click


    view = View()
    view.add_item(button)


    await inter.response.send_message(embed=embed, view=view)



bot.run(TOKEN)

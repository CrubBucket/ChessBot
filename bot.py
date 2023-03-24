import sys
import discord
from discord.ext import commands
from config import settings
from random import choice


bot = commands.Bot(command_prefix=settings['prefix'])
#client = discord.Client()





async def spam(channel):
    gena = await bot.fetch_user(00000000000)
    with open('games_to_comment.txt', 'r') as file:
        lines = file.readlines()
    for i in range(len(lines) - 2, 6, -9):
        name = lines[i - 7][:-1]
        op_name = lines[i - 6][:-1]
        result = lines[i - 5][:-1]
        color = lines[i - 4][:-1]
        time_control = lines[i - 3][:-1]
        rating = lines[i - 2][:-1]
        op_rating = lines[i - 1][:-1]
        game_id = lines[i][:-1]
        if result == 'lose':
            with open('lose_appeal.txt', 'r', encoding = 'UTF-8') as file:
                troll = file.readlines()
            main_output = f'{choice(troll[0:4])[0:-1]} {gena.mention} {choice(troll[4:8])[0:-1]} {choice(troll[8:12])[0:-1]} **{op_name}** в {time_control}! **{choice(troll[12:])[0:-1]}**'
            pts_output = f'Теперь у него всего лишь **{rating} PTS\'ов**, а у оппонента аж **{op_rating}!**'
            id_output = f'**ID каточки:** {game_id}'
            sus_output = discord.Embed(title="ЛУЗ!", description=main_output + '\n' + '\n' + pts_output + '\n' + '\n' + id_output, colour=0xf80000)
            await channel.send(embed=sus_output)
        if result == 'win':
            with open('win_appeal.txt', 'r', encoding = 'UTF-8') as file:
                troll = file.readlines()
            main_output = f'{choice(troll[0:4])[0:-1]} {gena.mention} {choice(troll[4:8])[0:-1]} {choice(troll[8:12])[0:-1]} **{op_name}** в {time_control}! **{choice(troll[12:])[0:-1]}**'
            pts_output = f'Теперь у него аж **{rating} PTS\'ов**, а у оппонента всего **{op_rating}!**'
            id_output = f'**ID каточки:** {game_id}'
            sus_output = discord.Embed(title="ВИН!",
                                       description=main_output + '\n' + '\n' + pts_output + '\n' + '\n' + id_output,
                                       colour=0x00e600)
            await channel.send(embed=sus_output)
        if result == 'draw':
            id_output = f'**ID каточки:** {game_id}'
            sus_output = discord.Embed(title="НИЧЬЯ!",
                                       description = f'У {gena.mention} и **{op_name}** письки оказались одного размера' '\n' + '\n' + id_output,
                                       colour=0x6c6874)
            await channel.send(embed=sus_output)
    sys.exit()


@bot.event
async def on_ready():
    print('Я в деле!\nP.S. {0.user}'.format(bot))
    text_channel_list = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            text_channel_list.append(channel)
    with open('channel_id.txt', 'r') as file:
        channel_id = file.read()
        if channel_id == '':
            out = discord.Embed(title = 'Куда высерать?', description = 'Напиши **~suda #(канал для высеров) **', colour = 0x6699cc)
            await text_channel_list[0].send(embed = out)
        else:
            for guild in bot.guilds:
                for channel in guild.text_channels:
                    if channel.id == int(channel_id):
                        await spam(channel)


@bot.command()
async def suda(ctx, channel: discord.TextChannel):
    with open('channel_id.txt', 'w') as file:
        file.write(str(channel.id))
    await channel.send('Ок')
    await spam(channel)


@bot.command()
async def test(ctx):
    print('Получил!')
    await ctx.send(f'Я в норме!')


bot.run(settings['token'])



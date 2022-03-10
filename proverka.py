import random
import json
import requests

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from config import settings

from include.discodb import DiscoDB
from include.discoapi import DiscoAPI

db = DiscoDB()
api = DiscoAPI()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

count = 0
pob = False

vopr = [[]]
nomervopr = 0

isTestStarted = False

qest = []
variant = []
globctx = ''
minevoprs = []
minerightanswers = []

with open('voprosy.txt', encoding='CP1251') as file:
    for line in file:
        vo = line.split('|')
        vopr.append([vo[0], vo[1]])

with open('test.txt') as test:
    cnt = 0
    quest = ''
    for line in test:
        if line.strip() != '@':
            if cnt == 0:
                quest += '\n' + line + '\n'
            else:
                quest += str(cnt) + ": " + line.replace('*', '')
            if '*' in line:
                minerightanswers.append(cnt)
            cnt += 1
        else:
            cnt = 0
            minevoprs.append(quest)
            quest = ''

author = ''


@bot.event
async def on_member_join(member):
    print('qqq')
    channel = bot.get_channel(885574933508411392)
    embed = discord.Embed(title="Привет!", description=f"{member.mention} только что присоединился")
    await channel.send(embed=embed)
    await member.send('**Привет, мы рады видеть тебя на нашем сервере! Приятного отдыха!**')


@bot.command()
async def starttest(ctx):
    global isTestStarted, globctx, minevoprs, author
    globctx = ctx
    author = ctx.message.author.nick
    await globctx.send('Тест начался.')
    isTestStarted = True
    try:
        await ctx.send(minevoprs[nomervopr])
    except Exception as ex:
        print(ex)


@bot.command()
async def stoptest(ctx):
    global isTestStarted
    isTestStarted = False
    await ctx.send('Тест завершен, спасибо за участие!')


rights = 0


@bot.event
async def on_message(message):
    try:
        global nomervopr, rights, count, isTestStarted
        await bot.process_commands(message)
        if len(
                message.content) > 1 and message.content != "%starttest" and author == message.author.nick and not message.author.bot and isTestStarted:
            isTestStarted = False
            await globctx.send('Вы вышли из теста)')
        if isTestStarted:
            if len(message.content) == 1:
                if message.content.isdigit():
                    if int(message.content) == minerightanswers[nomervopr]:
                        await globctx.send('**Правильно, маладэтс!!!**\n')
                        rights += 1
                    else:
                        await globctx.send('**Хорошая попытка(причем тут попыт?), но нэт**\n')
                    nomervopr += 1
                    if nomervopr == len(minerightanswers) - 1:
                        zvan = ''
                        if rights <= 5:
                            zvan = 'Полный нуб'
                        elif 5 < rights <= 10:
                            zvan = 'Нуб'
                        elif 10 < rights <= 15:
                            zvan = 'Почти про'
                        elif 15 < rights <= 20:
                            zvan = 'Про'

                        predl = 'Ты молодец. Ты ответил на ' + str(rights) + 'вопросов и получаешь звание: ' + zvan
                        await globctx.send(predl)
                        isTestStarted = False
                        nomervopr = 0
                    else:
                        await starttest(globctx)
    except Exception as ex:
        print(ex)


@bot.command()
async def hi(ctx):
    try:
        await ctx.send('Привет, я твой бот. Введи комманду %help чтобы узнать что я умею. '
                       'Если ты введешь %help_po_db и название комманды, выведется полная документация по этой '
                       'комманде.')
    except Exception as ex:
        print(ex)


@bot.command()
async def golosovanie(ctx, *, message):
    try:
        await ctx.message.delete()
        msgage = await ctx.send(message)
        await msgage.add_reaction('👍')
        await msgage.add_reaction('👎')
    except Exception as ex:
        print(ex)


@bot.command()
async def help_po_db(ctx, command: str):
    global count, sel
    try:
        sel = db.getcommandhelp(command)
    except Exception as ex:
        print(ex)
    msg = ' - '.join(sel)
    await ctx.send(msg)
    count += 1


@bot.command()
async def vopros(ctx):
    global nomervopr
    try:
        l = random.randint(0, len(vopr) - 1)
        nomervopr = l
        await ctx.send(vopr[l][0])
    except Exception as ex:
        print(ex)


@bot.command()
async def otvet(ctx, msg: str):
    try:
        if msg.strip() == vopr[nomervopr][1].strip():
            await ctx.send('Правильно, маладэц!')
        else:
            await ctx.send('Не угадал, попробуй ещё')
    except Exception as ex:
        print(ex)


@bot.command()
async def neznau(ctx):
    try:
        await ctx.send('Правильный ответ был: ' + vopr[nomervopr][1])
    except Exception as ex:
        print(ex)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    global count
    try:
        if amount <= 100:
            amount = int(amount)
            await ctx.channel.purge(limit=amount + 1)
            emb = discord.Embed(title="Чат был очищен", colour=discord.Color.purple())
            await ctx.send(embed=emb, delete_after=10)
            count += 1
        else:
            amount = 100000000
            await ctx.channel.purge(limit=amount + 1)
            emb = discord.Embed(title="Чат был очищен", colour=discord.Color.purple())
            await ctx.send(embed=emb, delete_after=10)
            count += 1
    except Exception as ex:
        print(ex)


@bot.command()
async def roll(ctx, dice: str):
    global count
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Формат должен быть, например 1d4')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)
    count += 1


@bot.command()
async def sum(ctx, One: int, Two: int):
    global count
    try:
        await ctx.send(One + Two)
        count += 1
    except Exception as ex:
        print(ex)


@bot.command()
async def mult(ctx, One: int, Two: int):
    global count
    try:
        count += 1
        await ctx.send(One * Two)
    except Exception as ex:
        print(ex)


@bot.command()
async def minus(ctx, One: int, Two: int):
    global count
    count += 1
    await ctx.send(One - Two)


@bot.command()
async def delit(ctx, One: int, Two: int):
    global count
    try:
        count += 1
        await ctx.send(One / Two)
    except Exception as ex:
        print(ex)


@bot.command()
async def youtube(ctx, *, finds):
    global count
    try:
        count += 1
        results = api.youtube(finds)
        await ctx.send('https://www.youtube.com/watch?v=' + results[0])
    except Exception as ex:
        print(ex)


@bot.command()
async def server(ctx):
    global count
    try:
        count += 1
        owner = str(ctx.guild.owner)
        region = str(ctx.guild.region)
        guild_id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        desc = ctx.guild.description

        embed = discord.Embed(
            title=ctx.guild.name + " Информация о сервере",
            description=desc,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Владелец", value=owner, inline=True)
        embed.add_field(name="ID сервера", value=guild_id, inline=True)
        embed.add_field(name="Регион", value=region, inline=True)
        embed.add_field(name="Количество участников", value=memberCount, inline=True)

        await ctx.send(embed=embed)

        members = []
        async for member in ctx.guild.fetch_members(limit=150):
            await ctx.send('Имя: {}\t Статус: {}\n Присоединился {}'.format(member.display_name, str(member.status),
                                                                            str(member.joined_at)))
    except Exception as ex:
        print(ex)


@bot.command()
async def check(ctx):
    global count
    try:
        count += 1
        await ctx.send('♟ мат ♟')
    except Exception as ex:
        print(ex)


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    global count
    try:
        count += 1
        await ctx.message.delete()
        await member.kick(reason=reason)
        emb = discord.Embed(title=f"Пользователь, под именем {member.name}, был кикнут!",
                            colour=discord.Color.dark_gold())
        await ctx.send(embed=emb)
    except Exception as ex:
        print(ex)


@bot.event
async def on_command_error(ctx, error):
    global count
    try:
        count += 1
        if isinstance(error, CommandNotFound):
            await ctx.send('Ты ввел не ту комманду!!!')
    except Exception as ex:
        print(ex)


@bot.command()
async def hello(ctx):
    global count
    try:
        count += 1
        author = ctx.message.author
        await ctx.send(f'Привет, {author.mention}!')
    except Exception as ex:
        print(ex)


@bot.command()
async def bye(ctx):
    global count
    try:
        count += 1
        author = ctx.message.author
        await ctx.send(f'Пока, {author.mention}!')
    except Exception as ex:
        print(ex)


@bot.command()
async def tts(ctx, msg):
    try:
        await ctx.send(msg, tts=True)
    except Exception as ex:
        print(ex)


@bot.event
async def on_command(ctx):
    server = ctx.guild.name
    user = ctx.author
    command = ctx.command
    try:
        db.logcommand(user, command)
    except Exception as ex:
        print(ex)


@bot.command()
async def last10(ctx):
    try:
        sel = db.getlast10commands()
        coms = []
        coms.append('Последние 10 команд: ')
        for s in sel:
            coms.append('Юзер: ' + str(s[0]) + '   Команда: ' + str(s[1]))
        await ctx.send('\n'.join(coms))
    except Exception as ex:
        print(ex)


@bot.command()
async def role(ctx, member: discord.Member, role: discord.Role):
    try:
        await member.add_roles(role)
    except Exception as ex:
        print(ex)


@bot.command()
async def fox(ctx):
    global count
    try:
        count += 1
        response = api.fox()
        json_data = json.loads(response.text)
        embed = discord.Embed(color=0xff9900, title='Лися')
        embed.set_image(url=json_data['link'])
        await ctx.send(embed=embed)
    except Exception as ex:
        print(ex)


@bot.command()
async def anime(ctx):
    global count
    try:
        count += 1
        response = api.anime()
        json_data = json.loads(response.text)
        embed = discord.Embed(color=0xff9900, title='Animeeeee')
        embed.set_image(url=json_data['link'])
        await ctx.send(embed=embed)
    except Exception as ex:
        print(ex)


@bot.command()
async def anime2(ctx):
    global count
    try:
        count += 1
        response = api.anime2()
        json_data = json.loads(response.text)
        embed = discord.Embed(color=0xff9900, title='Animeeeee')
        embed.set_image(url=json_data['link'])
        await ctx.send(embed=embed)
    except Exception as ex:
        print(ex)


@bot.command()
async def dog(ctx):
    global count
    try:
        count += 1
        response = requests.get('https://some-random-api.ml/img/dog')
        json_data = json.loads(response.text)

        embed = discord.Embed(color=0xff9900, title='Собяка')
        embed.set_image(url=json_data['link'])
        await ctx.send(embed=embed)
    except Exception as ex:
        print(ex)


@bot.command()
async def parthner(ctx):
    global count
    try:
        count += 1
        embed = discord.Embed(
            title="Тык для перехода",
            description="Ссылка для перехода на сервера моих друзей человегов:",
            url='https://discord.gg/2gBh6W7ye2')
        await ctx.send(embed=embed)
    except Exception as ex:
        print(ex)


@bot.command()
async def parthner2(ctx):
    global count
    try:
        count += 1
        embed = discord.Embed(
            title="Тык для перехода",
            description="Ссылка для перехода на сервера моих друзей человегов:",
            url='https://discord.gg/FBGkd8RR4X')
        await ctx.send(embed=embed)
    except Exception as ex:
        print(ex)


@bot.event
async def on_ready():
    while True:
        game = discord.Game("Майнкрафт на сервере \n CUBECRAFT")
        await bot.change_presence(status=discord.Status.idle, activity=game)


bot.run(settings['token'])

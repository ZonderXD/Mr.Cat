import discord
import os
import asyncio
import datetime
import random as r
import random
import io
import youtube_dl
import youtube_dl, os
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'          [Mr.BlackCatBot]')
    type = discord.ActivityType.watching
    activity = discord.Activity(name = "за сервером Mr.BlackCat", type = type)
    status = discord.Status.online
    await bot.change_presence(activity = activity, status = status)
    print(f"[Mr.BlackCatBot] Bot successfully launched!;")
    print(f"[Mr.BlackCatBot] Name: [{bot.user}];")
    print(f'[Mr.BlackCatBot] ID: [{bot.user.id}]')
    print('[------------------------------]')
    print(f'          [Other]')

@bot.event
async def is_owner(ctx):
    return ctx.author.id == 668325441224048641 # Айди создателя бота
    return ctx.author.id == 475239960778244097

@bot.command()
async def server(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name}", description=f"Сервер создали: {guild.created_at.strftime('%b %#d, %Y')}\n\n"
                                                             f"Регион: {guild.region}\n\nГлава сервера: {guild.owner}\n\n"
                                                             f"Людей на сервере: {guild.member_count}\n\n",  color=0xff0000,timestamp=ctx.message.created_at)

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {guild.id}")

    embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
    await ctx.send(embed=embed)

@bot.command(aliases=['подключиться', 'j', 'jo'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice is not None:
        return await voice.move_to(channel)
    else:
        await channel.connect()
        await ctx.send(embed = discord.Embed(description = f"**Я успешно подключился к голосовому каналу <#{channel.id}> !**", color=0xdbf2))


@bot.command(aliases=['отключиться', 'l'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(embed = discord.Embed(description = f"**Я успешно отключился от голосового канала <#{channel.id}> !**", color=0xdbf2))
    else:
        await ctx.send(embed = discord.Embed(description = f"**Извините, но я не находжусь в голосовом канале.**", color=0xdbf2))


@bot.command()
async def play(ctx, url : str):
    song_there = os.path.isfile('song.mp3')

    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Старый файл удален')
    except PermissionError:
        print('[log] Не удалось удалить файл')

    await ctx.send(embed = discord.Embed(description = f'**Пожалуйста подождите я загружаю Вашу музыку.**', color=0xdbf2))

    voice = get(bot.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Загружаю музыку...')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'[log] Переименовываю файл: {file}')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, музыка закончила свое проигрывание'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    song_name = name.rsplit('-', 2)
    await ctx.send(embed = discord.Embed(description = f'**Сейчас играет музыка - `{song_name[0]}`. Приятного прослушивания.**', color=0xdbf2))

@bot.command(aliases=['пауза', 'p'])
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.pause()
        await ctx.send(embed = discord.Embed(description = f"**Музыка была поставлена на паузу.**", color=0xdbf2))
    else:
        await ctx.send(embed = discord.Embed(description = f"**Извините но музыка и так на паузе.**", color=0xdbf2))


@bot.command(aliases=['продолжить', 'r'])
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        voice.resume()
        await ctx.send(embed = discord.Embed(description = f"**Музыка продолжается.**", color=0xdbf2))
    else:
        await ctx.send(embed = discord.Embed(description = f"**Извините, но музыка не на паузе.**", color=0xdbf2))

@bot.command(aliases=['громкость', 'v'])
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.send(embed = discord.Embed(description = f"**Извините, но я не подключён к голосовому каналу.**", color=0xdbf2))
    ctx.voice_client.source.volume = volume / 100
    await ctx.send(embed = discord.Embed(description = f"**Громкость изменена на {volume}%**", color=0xdbf2))

@bot.event
async def on_member_join(member):
	await member.create_dm()
	
	await member.send(embed = discord.Embed(description = f'**<@{member.id}> Приветствую тебя на сервере `{member.guild.name}` ! Желаю тебе хорошо повеселится. И обязательно прочитай правила сервера!**', color=0xec33))

@bot.command()
async def password(ctx, lenght: int = None, number: int = None):

    if not lenght or not number:
        await ctx.send(embed = discord.Embed(description = f'Пожалуйста, укажите длину пароля и количество символов в нем.', color=0x0c0c0c)) 

    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for x in range(number):
        password = ''

        for i in range( lenght ):
            password += random.choice(chars)

        await ctx.author.send(embed = discord.Embed(description = f'**Сгенерированный пароль:\n{password}**', color=0x0c0c0c)) 
        await ctx.send(embed = discord.Embed(description = f'**Пароль успешно отправлен!**', color=0x0c0c0c))
        return

@bot.command()
async def help(ctx):
	emb = discord.Embed( title = 'Команды:', color=0x6fdb9e )

	emb.add_field(name='Информационные:', value='``.user`` - Узнать информацию о пользователе\n ``.role`` - Информация о роли\n ``.server`` - Узнать информацию о сервере', inline = False)
	emb.add_field(name='Администрация:', value='`.ban` - Бан пользователя\n `.kick` - Кикнуть пользователя\n `.mute` - Замутить пользователя\n `.unmute` - Размутить пользователя\n `.tempban` - Временный бан\n `.tempmute` - Временный мут\n `.clear` - Очистить сообщения\n `.rename` - Поменять ник',inline = False)
	emb.add_field(name='Экономия:', value='``.work`` - Пойти на работу\n ``.bank`` - Проверить баланс',inline = False)
	emb.add_field(name='Разное:', value=' ``.avatar`` - Аватар пользоватлея\n ``.ping`` - Пинг бота\n ``.time`` - Узнать время\n ``.roles`` - Узнать сколько пользователей с ролью',inline = False)
	emb.add_field(name='Музыка:', value='`.join` - Вход бота в гл. канал\n `.leave` - Выход бота из гл. канала\n `.play` - Вкл. музыку\n `.pause` - Пауза\n `.resume` - Продолжить музыку\n `.volume` - Громкость',inline = False)
	emb.add_field(name='Весёлости:', value='``.ran_color`` - Рандомный цвет в формате HEX\n ``.coin`` - Бросить монетку\n ``.math`` - Решить пример\n `.8ball` - Волшебный шар\n `.password` - Рандомный',inline = False)
	emb.set_thumbnail(url=ctx.guild.icon_url)
	emb.set_footer(text='Mr.FireCat#8064 © | Все права защищены', icon_url='https://cdn.discordapp.com/avatars/475239960778244097/023e2fe1a2ce5eee97c98c9e4c83106e.webp?size=1024')

	await ctx.send( embed = emb )

@bot.command()
async def user(ctx, Member: discord.Member = None ):
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация о пользователе.'.format(Member.name), description=f"Участник зашёл на сервер: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
                                                                                      f"Имя: {Member.name}\n\n"
                                                                                      f"Никнейм: {Member.nick}\n\n"
                                                                                      f"Статус: {Member.status}\n\n"
                                                                                      f"ID: {Member.id}\n\n"
                                                                                      f"Высшая роль: {Member.top_role}\n\n"
                                                                                      f"Аккаунт создан: {Member.created_at.strftime('%b %#d, %Y')}", 
                                                                                      color=0xff0000, timestamp=ctx.message.created_at)

    emb.set_thumbnail(url= Member.avatar_url)
    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

@bot.command()
async def avatar(ctx, member : discord.Member = None):

    user = ctx.message.author if (member == None) else member

    embed = discord.Embed(title=f'Аватар пользователя {user}', color= 0x0c0c0c)

    embed.set_image(url=user.avatar_url)

    await ctx.send(embed=embed)

@bot.command()
async def coin( ctx ):
    coins = [ 'орел', 'решка' ]
    coins_r = random.choice( coins )
    coin_win = 'орел'

    if coins_r == coin_win:
        await ctx.send(embed = discord.Embed(description= f''':tada: { ctx.message.author.name }, выиграл! 
            Тебе повезло у тебя: ``{ coins_r }``''', color = 0x0c0c0c))

    if coins_r != coin_win:
        await ctx.send(embed = discord.Embed(description= f''':thumbsdown:  { ctx.message.author.name }, проиграл! 
            Тебе не повезло у тебя: ``{ coins_r }``''', color = 0x0c0c0c))

@bot.command()
async def ping(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    emb = discord.Embed(
        title= 'Текущий пинг',
        description= f'{bot.ws.latency * 1000:.0f} ms'
    )
    await ctx.send(embed=emb)

@bot.command()
async def time(ctx):
    emb = discord.Embed(colour= discord.Color.green(), url= 'https://www.timeserver.ru')
    
    emb.set_author(name= bot.user.name, icon_url=bot.user.avatar_url)
    emb.set_footer(text= 'Если у вас время по МСК, то к этому добавляйте +1 час', icon_url=ctx.author.avatar_url)
    emb.set_thumbnail(url='https://www.worldtimeserver.com/img/dst/dst-2-3.png')

    now_date = datetime.datetime.now()
    emb.add_field(name='Time', value='{}'.format(now_date))

    await ctx.send( embed = emb )

@bot.command()
async def ran_color(ctx):
    clr = (random.randint(0,16777215))
    emb = discord.Embed(
        description= f'Сгенерированый цвет : ``#{hex(clr)[2:]}``',
        colour= clr
    )

    await ctx.send(embed=emb)

@bot.command()
@commands.has_permissions( administrator = True) 
async def tempban(ctx, member : discord.Member, time:int, arg:str, *, reason=None):
    if member == ctx.message.author:
        return await ctx.send("Ты не можешь забанить сам себя.")
    msgg =  f'Пользователь <@{member.id}> , забанен по причине {reason}.'
    msgdm = f'Вы были забанены на сервере {ctx.guild.name}, по причине {reason}.'
    if reason == None:
        msgdm = f'Вы были забанены на сервере {ctx.guild.name}.'
    if reason == None:
        msgg =  f'Пользователь <@{member.id}>, забанен.'
    await ctx.send(msgg)  
    await member.send(msgdm)
    await ctx.guild.ban(member, reason=reason)
    if arg == "s":
        await asyncio.sleep(time)          
    elif arg == "m":
        await asyncio.sleep(time * 60)
    elif arg == "h":
        await asyncio.sleep(time * 60 * 60)
    elif arg == "d":
        await asyncio.sleep(time * 60 * 60 * 24)
    await member.unban()
    await ctx.send(f'Пользователь <@{member.id}> , разбанен.')
    await member.send(f'Вы были разбанены на сервере {ctx.guild.name}')

@bot.command(name = "8ball")
async def ball(ctx, *, arg):

    message = ['Нет','Да','Возможно','Опредленно нет'] 
    s = random.choice( message )
    await ctx.send(embed = discord.Embed(description = f'**:crystal_ball: Знаки говорят:** {s}', color=0x0c0c0c))
    return

# Работа с ошибками шара

@ball.error 
async def ball_error(ctx, error):

    if isinstance( error, commands.MissingRequiredArgument ): 
        await ctx.send(embed = discord.Embed(description = f'Пожалуйста, укажите вопрос.', color=0x0c0c0c)) 

@bot.command()
@commands.has_permissions( administrator = True) 
async def tempmute(ctx,amount : int,member: discord.Member = None, reason = None):
    mute_role = discord.utils.get(member.guild.roles, id = 666994837790261278) #Айди роли
    channel_log = bot.get_channel(670260939249156096) #Айди канала логов

    await member.add_roles( mute_role )
    await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
    await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c))
    await asyncio.sleep(amount)
    await member.remove_roles( mute_role ) 

@bot.command()
@commands.has_permissions( administrator = True) 
async def ban(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:
        
        channel_log = bot.get_channel(670260939249156096) #Айди канала логов

        await member.ban( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0x0c0c0c)) 

# Работа с ошибками бана

@ban.error 
async def ban_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))  

# Работа с ошибками мута на время

@tempmute.error 
async def tempmute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

@bot.command()
@commands.has_permissions( administrator = True) 
async def kick(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        channel_log = bot.get_channel(670260939249156096) #Айди канала логов

        await member.kick( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0x0c0c0c))
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0x0c0c0c)) 

# Работа с ошибками кика

@kick.error 
async def kick_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

@bot.command()
@commands.has_permissions( administrator = True) 
async def mute(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите причину!**'))

    else:

        mute_role = discord.utils.get(member.guild.roles, id = 694191903972917319) #Айди роли

        await member.add_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c))   

# Работа с ошибками мута

@mute.error 
async def mute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

@bot.command()
@commands.has_permissions( administrator = True) 
async def unmute(ctx,member: discord.Member = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    else:

        mute_role = discord.utils.get(member.guild.roles, id = 694191903972917319) #Айди роли

        await member.remove_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был вернут доступ к чатам.**', color=0x0c0c0c))     

# Работа с ошибками размута

@unmute.error 
async def unmute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

@bot.command()
@commands.has_permissions( administrator = True)
async def clear(ctx,amount : int):
    

    await ctx.channel.purge( limit = amount )
    await ctx.send(embed = discord.Embed(description = f'**:heavy_check_mark: Удалено {amount} сообщений.**', color=0x0c0c0c))

# Работа с ошибками очистки чата

@clear.error 
async def clear_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**:grey_exclamation: {ctx.author.name},обязательно укажите количевство сообщений.**', color=0x0c0c0c))

@bot.command()
async def role(ctx, Role: discord.Role ):
    guild = ctx.guild
    emb = discord.Embed(title='Информация о роли .'.format(Role.name), description=f"Роль создали {Role.created_at.strftime('%b %#d, %Y')}\n\n"
                                                                                   f"Название роли: {Role.name}\n\nЦвет: {Role.colour}\n\n"
                                                                                   f"Позиция: {Role.position}\n\n",colour= Role.colour, timestamp=ctx.message.created_at)

    emb.set_footer(text=f"ID Пользователя: {ctx.author.id}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

@bot.command(name = "changename", aliases = ["rename", "change"])
@commands.has_permissions(kick_members = True)
async def changing_name(ctx, member: discord.Member = None, nickname: str = None):
    try:
        if member is None:
            await ctx.send(embed = discord.Embed(description = "Обязательно укажите **пользователя**!"))
        elif nickname is None:
            await ctx.send(embed = discord.Embed(description = "Обязательно укажите ник!"))
        else:
            await member.edit(nick = nickname)
            await ctx.send(embed = discord.Embed(description = f"У пользователя **{member.name}** был изменен ник на **{nickname}**"))
    except:
        await ctx.send(embed = discord.Embed(description = f"Я не могу изменить ник пользователя **{member.name}**!"))

@bot.command()
async def roles(ctx, role: discord.Role):
    await ctx.send(f'**Участников с этой ролью:** {len(role.members)}')

@bot.command(aliases = ['count', 'calc', 'вычисли', 'math'])
async def __count(ctx, *, args = None):
    text = ctx.message.content

    if args == None:
        await ctx.send(embed = discord.Embed(description = 'Пожалуйста, укажите выражение для оценки.', color = 0x39d0d6))
    else:
        result = eval(args)
        await ctx.send(embed = discord.Embed(description = f'Результат примера: `{args}`: \n`{result}`', color = 0x39d0d6))

@bot.command()
@commands.cooldown(5, 5, commands.BucketType.user)
async def work(ctx):

        await ctx.send(embed = discord.Embed(title="**:moneybag:Вы пошли на свою работу.:moneybag:**", colour=ctx.message.author.color))

        num = random.randint(1, 500)

        userid = ctx.message.author.id # id пользователя
        serverid = ctx.guild.id # id сервера
        color = ctx.message.author.color # цвет роли пользователя 

        ocount = f'{userid}{serverid}' # будет примерно так: 349790345204334594649246512328605700

        

        listdir = os.listdir(path="bank") # читаем папку bank 

        if f'{ocount}.cfg' in str(listdir):

                await asyncio.sleep(1)
                see = open(f'bank\\{ocount}.cfg','r')
                money = see.read()
                see.close() 

                new = int(money) + int(num)
                
                see = open(f'bank\\{ocount}.cfg','w')
                see.write(str(new))
                see.close()

                await ctx.send(embed = discord.Embed(title=f"**:moneybag:Вы заработали {num}.:moneybag:**", colour=color).set_thumbnail(url=ctx.message.author.avatar_url))
        else: 
                await ctx.send(embed = discord.Embed(title=f"**:moneybag:Вы ничего не заработали, сначала зарегестрируйте счет в банке.:moneybag:**", colour=color).set_thumbnail(url=ctx.message.author.avatar_url))

@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def bank(ctx):
        
        user = ctx.message.author 
        userid = ctx.message.author.id 
        serverid = ctx.guild.id
        servername = ctx.guild.name 
        color = ctx.message.author.color 

        ocount = f'{userid}{serverid}'

        

        listdir = os.listdir(path="bank") 

        if f'{ocount}.cfg' in str(listdir):
                
                see = open(f'bank\\{ocount}.cfg','r')
                money = see.read()
                see.close() 

                emb = discord.Embed(title="**:bank:Банк:bank:**", colour=color)
                emb.add_field(name="**Баланс:**", value=f"**:moneybag:{money}:moneybag:**", inline=False)
                emb.add_field(name="**Сервер:**", value=f"**:computer:{servername}:computer:**", inline=False)  
                emb.add_field(name="**Имя:**", value=f"**{str(user)[:-5]}**", inline=False) 
                emb.add_field(name="**Тег:**", value=f"**{str(user)[-4:]}**", inline=False) 

                await ctx.send(embed = emb)
        else:
                
                print('The member was registered.')
                print("[------------------------------]")
                print(f'          [Next]')

                reg= open(f'bank\\{ocount}.cfg','w')
                reg.write('50') # Начальная сумма
                reg.close()

                see = open(f'bank\\{ocount}.cfg','r')
                money = see.read()
                see.close()

                emb = discord.Embed(title="**:bank:Банк:bank:**", colour=color)
                emb.add_field(name="**Баланс:**", value=f"**:moneybag:{money}:moneybag:**", inline=False)
                emb.add_field(name="**Сервер:**", value=f"**:computer:{servername}:computer:**", inline=False)  
                emb.add_field(name="**Имя:**", value=f"**{str(user)[:-5]}**", inline=False) 
                emb.add_field(name="**Тег:**", value=f"**{str(user)[-4:]}**", inline=False) 

                await ctx.send(embed = emb)



token = open( 'token.txt', 'r' ).readline()
bot.run( token )
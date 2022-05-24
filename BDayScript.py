from time import localtime, time

import random
import hikari
import lightbulb
from lightbulb.ext import tasks

bot = lightbulb.BotApp(token='OTcyNjU4OTk0NTQxODkxNjM0.Gv4BqK.f92vxriun58x72N-rBYvzjOTfAoTKc3r9hJunY', prefix= "!", intents = hikari.Intents.ALL)
Time = localtime(time())

sayings = open('Sayings','r')
saying = sayings.read()
say_lst = saying.split("\n")

tasks.load(bot)

@tasks.task(h=1, auto_start= True)
async def check():
    await message('x')

@bot.listen()
async def message(event: hikari.StartedEvent):
    file =  open('B-DayList', 'r')
    data = file.read()
    data_lst = data.split("\n")

    nested_data = [i.split(' ') for i in data_lst]

    guild_file = open('GuildList', 'r')
    guild_read = guild_file.read()
    guild_lst = guild_read.split('\n')

    channel_file = open('ChannelList', 'r')
    channel_read = channel_file.read()
    channel_lst = channel_read.split('\n')

    guild_channel_dic = dict(zip(guild_lst, channel_lst))

    for i in nested_data:
        if len(i) > 1 and Time[1] == int(i[0]) and Time[2] == int(i[1]):
            random_int = random.randint(0,29)
            set_channel = guild_channel_dic[i[3]]
            await bot.rest.create_message(set_channel, f'<@{i[2]}> {say_lst[random_int]}', user_mentions= True)
    
    file.close()
    guild_file.close()
    channel_file.close()

@bot.command
@lightbulb.option('month', "Birth Month (mm)")
@lightbulb.option('day', 'Birth Day (dd)')
@lightbulb.option('user', 'Whose birth day (User ID)')
@lightbulb.command('bday', 'Add a new birthdate')
@lightbulb.implements(lightbulb.SlashCommand)
async def bday(ctx):
    current_channel = ctx.get_channel()

    if not bot.cache.get_member(ctx.get_guild(), ctx.options.user):
        await bot.rest.create_message(current_channel, "Error: User not found in server")
        await ctx.respond("...")
        return
    
    try:
        int(ctx.options.day) and int(ctx.options.day)
    except:
        await bot.rest.create_message(current_channel, "Error: Please input numbers")
        await ctx.respond("...") 
        return

    if int(ctx.options.month) > 12 or int(ctx.options.day) > 31:
        await bot.rest.create_message(current_channel, "Error: Invalid month or day")
        await ctx.respond("...")
        return

    if len(ctx.options.month) < 2 or len(ctx.options.day) < 2:
        await bot.rest.create_message(current_channel, "Error: Please follow mm/dd format")
        await ctx.respond("...")
        return

    guild_file = open('GuildList', 'r')
    guild_read = guild_file.read()
    guild_lst = guild_read.split('\n')

    if not str(ctx.get_guild().id) in guild_lst:
        await bot.rest.create_message(current_channel, "Error: Server not set up")
        await ctx.respond("...") 
        return

    channel_file = open('ChannelList', 'r')
    channel_read = channel_file.read()
    channel_lst = channel_read.split('\n')

    guild_channel_dic = dict(zip(guild_lst, channel_lst))

    guild_file.close()
    channel_file.close()

    set_channel = guild_channel_dic[str(ctx.get_guild().id)]

    file = open('B-DayList', 'a')
    file.write(f'{ctx.options.month} {ctx.options.day} {ctx.options.user} {ctx.get_guild().id}\n')
    await ctx.respond("Yay!")
    await bot.rest.create_message(set_channel, "Birthdate added")
    file.close()

@bot.command
@lightbulb.option('channel', 'Input channel ID')
@lightbulb.command('setup', 'For new servers (required)')
@lightbulb.implements(lightbulb.SlashCommand)
async def setup(ctx):
    current_channel = ctx.get_channel()

    guild_file = open('GuildList', 'r')
    guild_read = guild_file.read()
    guild_lst = guild_read.split('\n')

    if str(ctx.get_guild().id) in guild_lst:
        await bot.rest.create_message(current_channel, "Error: Server already set up")
        await ctx.respond("...")
        return
    
    guild_file.close()

    channels_in_guild = bot.cache.get_guild_channels_view_for_guild(ctx.get_guild()).keys()
    lst = [i for i in channels_in_guild]
    if not int(ctx.options.channel) in lst:
        await bot.rest.create_message(ctx.get_channel(), "Error: Channel not found in server")
        await ctx.respond("...") 
        return
    
    guild_file = open('GuildList', 'a')
    guild_file.write(f'{ctx.get_guild().id}\n')
    guild_file.close()

    channel_file = open('ChannelList', 'a')
    channel_file.write(f'{ctx.options.channel}\n')
    channel_file.close()

    await ctx.respond("Yay!")
    await bot.rest.create_message(ctx.get_channel(), "Setup complete")

@bot.command
@lightbulb.option('user', "Input user ID")
@lightbulb.command('delete', 'Delete user bday')
@lightbulb.implements(lightbulb.SlashCommand)
async def delete(ctx):
    with open('B-DayList', 'r') as f:
        lines = f.readlines()
    with open('B-DayList', 'w') as f:
        for line in lines:
            if not str(ctx.options.user) in line:
                f.write(line)

    await ctx.respond("Yay!")
    await bot.rest.create_message(ctx.get_channel(), "User deleted")
    f.close()

@bot.command
@lightbulb.option('channel', 'new channel ID')
@lightbulb.command('reset', 'set new channel')
@lightbulb.implements(lightbulb.SlashCommand)
async def reset(ctx):


    guild_file = open('GuildList', 'r')
    guild_read = guild_file.read()
    guild_lst = guild_read.split('\n')

    if not str(ctx.get_guild().id) in guild_lst:
        await bot.rest.create_message(ctx.get_channel(), "Error: Server not set")
        await ctx.respond("...")
        return

    channel_file = open('ChannelList', 'r')
    channel_read = channel_file.read()
    channel_lst = channel_read.split('\n')

    guild_channel_dic = dict(zip(guild_lst, channel_lst))
    current_channel = guild_channel_dic[str(ctx.get_guild().id)]

    guild_file.close()
    channel_file.close()

    with open('GuildList', 'r') as f:
        lines = f.readlines()
    with open('GuildList', 'w') as f:
        for line in lines:
            if not str(ctx.get_guild().id) in line:
                f.write(line)
        f.write(f'{ctx.get_guild().id}\n')  
        f.close()

    with open('ChannelList', 'r') as f:
        lines = f.readlines()
    with open('ChannelList', 'w') as f:
        for line in lines:
            if not current_channel in line:
                f.write(line)
        f.write(f'{ctx.options.channel}\n')
        f.close()

    await ctx.respond("Yay!")
    await bot.rest.create_message(ctx.get_channel(), "New channel set")

@bot.command
@lightbulb.command('list', "shows a list of registered users in your server")
@lightbulb.implements(lightbulb.SlashCommand)
async def xlist(ctx):
    file =  open('B-DayList', 'r')
    data = file.read()
    data_lst = data.split("\n")

    nested_data = [i.split(' ') for i in data_lst]

    await ctx.respond("Yay!")
    for whole_data in nested_data:
        if str(ctx.get_guild().id) in whole_data and len(whole_data) > 1:
            user = bot.cache.get_user(int(whole_data[2]))
            await bot.rest.create_message(ctx.get_channel(),f"Month: {int(whole_data[0])} Day: {int(whole_data[1])} User: {user.username}")    
    file.close()
bot.run()
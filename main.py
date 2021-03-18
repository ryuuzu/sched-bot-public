import discord
import json
import logging
import pytz
import os
from dotenv import load_dotenv
from datetime import datetime as dt
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix= ".")
NST = pytz.timezone('Asia/Kathmandu')
with open("schedule.json", 'r') as f:
    allsched = json.load(f)
with open("student.json", "r") as f:
    students = json.load(f)
bot.remove_command('help')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name = "in Islington College"))
    print(f"{bot.user.name} is ready to rock.")

@bot.command(aliases = ['help', 'commands'])
async def cmds(ctx):
    embed = discord.Embed(title = "Help and Commands", description = "Hello, I am a basic schedule bot that will provide you with your class schedules for the day. My prefix is `.`")
    embed.set_thumbnail(url = bot.user.avatar_url_as(format = "png", size = 512))
    embed.add_field(name = "nextclass", value = "(also nc) Look for your next class from the schedule.")
    embed.add_field(name = "schedule", value = "(also sch) Look for your schedule for the day.")
    embed.add_field(name = "lookup", value = "(also lu) Lookup Student Info by someone's name/id.")
    embed.set_footer(text = "The schedule data were collected and stored as json files.")
    await ctx.send(embed= embed)

@bot.command(aliases = ['nc'])
async def nextclass(ctx, group:str = None):
    author = ctx.author
    # if day is None:
    day = dt.strftime(dt.now(NST), "%a")
    day = day.upper()
    if group == None:
        specialization = author.top_role.name
        group = getGroupname(author.roles)
    elif group.startswith("C") or group.startswith("c"): 
        specialization = "Computing"
    elif group.startswith("M") or group.startswith("m"): 
        specialization = "Multimedia Technologies"
    elif group.startswith("N") or group.startswith("n"): 
        specialization = "Computer Networking & IT Security"
    group = group.upper()
    today = []
    try:
        routine = allsched[specialization][group]
    except KeyError:
        await ctx.send("Group not found.")
    for period in routine:
        if period['Day'] == day:
            today.append(period)
    time = dt.strftime(dt.now(NST), "%I:%M%p")
    a = dt.strptime(time, "%I:%M%p")
    for period in today:
        start = period['Time'][:8]
        print(start)
        b = dt.strptime(start, "%I:%M %p")
        if b > a:
            timerem = b - a
            embed = discord.Embed(title = f"{period['Module Code']} - {period['Module Title ']}", color = discord.Colour.dark_blue())
            embed.set_thumbnail(url = bot.user.avatar_url_as(format = "png", size = 128))
            embed.add_field(name = "Class Type", value = period['Class Type'])
            embed.add_field(name = "Lecturer", value = period['Lecturer'])
            embed.add_field(name = "Time", value = period['Time'], inline = False)
            return await ctx.send(content = f'Your next class is in {timerem.seconds/60} minutes.\nHere are the class details', embed = embed)
    else:
        return await ctx.send("Looks like you have no classes today. But I might be wrong, who knows.")

@bot.command(aliases = ['lu'])
async def lookup(ctx, *, name):
    data = []
    for course in students.keys():
        coursedat = students[course]
        for group in coursedat.keys():
            groupdat = coursedat[group]
            for student in groupdat:
                name1 = student['name']
                id = student['id']
                try:
                    keyword = int(name)
                except ValueError:
                    keyword = name
                if isinstance(keyword, int):
                    if keyword == id:
                        data.append(student)
                else:
                    if keyword.upper() == name1:
                        data.append(student)
    if len(data) == 0: 
        return await ctx.send(f"There is no student with name {name}. Make sure you spelled it correctly.")
    msg = f"I found {len(data)} student/s with that name."
    await ctx.send(msg)
    for x in data:
        embed = discord.Embed(color = discord.Colour.dark_blue())
        embed.set_thumbnail(url = bot.user.avatar_url_as(format = "png", size = 128))
        embed.add_field(name = "Name", value = x['name'], inline = False)
        embed.add_field(name = "London Met ID", value = x['id'])
        embed.add_field(name = "Group", value = x['group'])
        embed.set_footer(text = "If the id is null, there was no id data when it was collected.")
        await ctx.send(embed=  embed)
    pass

@bot.command(aliases = ['sch'])
async def schedule(ctx, day:str = None, group:str = None):
    author = ctx.author
    if day is None:
        day = dt.strftime(dt.now(NST), "%a")
    day = day.upper()
    if group == None:
        specialization = author.top_role.name
        group = getGroupname(author.roles)
    elif group.startswith("C") or group.startswith("c"): 
        specialization = "Computing"
    elif group.startswith("M") or group.startswith("m"): 
        specialization = "Multimedia Technologies"
    elif group.startswith("N") or group.startswith("n"): 
        specialization = "Computer Networking & IT Security"
    group = group.upper()
    today = []
    try:
        routine = allsched[specialization][group]
    except KeyError:
        await ctx.send("Looks like something is wrong.\nGroup not found.")
    # day = dt.strftime(dt.now(NST), "%a").upper()
    for period in routine:
        if period['Day'] == day:
            today.append(period)
    if len(today) == 0: return await ctx.send("You have no classes on this day.")
    msg = f"You have **{len(today)}** classes."
    await ctx.send(msg)
    for x in today:
        embed = discord.Embed(title = f"{x['Module Code']} - {x['Module Title']}", color = discord.Colour.dark_blue())
        embed.set_thumbnail(url = bot.user.avatar_url_as(format = "png", size = 128))
        embed.add_field(name = "Class Type", value = x['Class Type'])
        embed.add_field(name = "Lecturer", value = x['Lecturer'])
        embed.add_field(name = "Time", value = x['Time'])
        embed.add_field(name = "Block", value = x['Block'])
        embed.add_field(name = "Room", value = x['Room'])
        await ctx.send(embed = embed)

def getGroupname(roles):
    for role in roles:
        if len(role.name) > 4:
            continue
        if role.name.startswith("C") or role.name.startswith("M") or role.name.startswith("N"):
            names = role.name.split("-")
            groupName = "".join(names)
            return groupName



bot.run(TOKEN)
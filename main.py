import discord
import json
import logging
from datetime import datetime as dt
from discord.ext import commands


bot = commands.Bot(command_prefix= ".")
with open("schedule.json", 'r') as f:
    allsched = json.load(f)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready to rock.")

@bot.command(aliases = ['nc'])
async def nextclass(ctx, group:str = None):
    author = ctx.author
    specialization = author.top_role
    if group == None:
        for x in author.role:
            if x.name.startswith("C") or x.name.startswith("M") or x.name.startswith("N"):
                group = x.name
                break
    group = group.upper()
    today = []
    try:
        routine = specialization[group]
    except KeyError:
        await ctx.send("Group not found.")
    day = dt.strftime(dt.now(), "%a").upper()
    for period in routine:
        if period['Day'] == day:
            today.append(period)
    

@bot.command(aliases = ['sch'])
async def schedule(ctx, group:str = None):
    author = ctx.author
    specialization = author.top_role
    if group == None:
        for x in author.role:
            if (x.name.startswith("C") and len(x.name) == 2) or (x.name.startswith("M") and len(x.name) == 2) or (x.name.startswith("N") and len(x.name) == 2):
                group = x.name
                break
    group = group.upper()
    today = []
    try:
        routine = specialization[group]
    except KeyError:
        await ctx.send("Group not found.")
    day = dt.strftime(dt.now(), "%a").upper()
    for period in routine:
        if period['Day'] == day:
            today.append(period)
    if len(today) == 0: return await ctx.send("You have no classes today.")
    msg = f"You have **{len(today)}** classes today."
    await ctx.send(msg)
    for x in today:
        embed = discord.Embed(title = f"{x['Module Code']} - {x['Module Title ']}", color = discord.Colour.dark_blue())
        embed.add_field(name = "Class Type", value = x['Class Type'])
        embed.add_field(name = "Lecturer", value = x['Lecturer'])
        embed.add_field(name = "Time", value = x['Time'])
        # embed.add_field(name = "Block", value = x['Block'])
        # embed.add_field(name = "Room", value = x['Room'])
        await ctx.send(embed = embed)





bot.run('ODE3OTgyMTE0NjkxMTUzOTIx.YERbNQ.QjnxcYpwmhgNMxgrhFvs0OZsLcU')
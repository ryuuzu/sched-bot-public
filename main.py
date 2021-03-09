import discord
from datetime import datetime as dt
import json
from discord.ext import commands


bot = commands.Bot(command_prefix= ".")
with open("schedule.json", 'r') as f:
    allsched = json.load(f)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready to rock.")

@bot.command(aliases = ['sch'])
async def schedule(ctx, group:str):
    group = group.capitalize()
    today = []
    try:
        routine = allsched[group]
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
        embed.add_field(name = "Block", value = x['Block'])
        embed.add_field(name = "Room", value = x['Room'])
        await ctx.send(embed = embed)





bot.run('NDAwNjg4NzY0MTM5MjA4NzE0.WlZAfQ.p3BrakR71bK9Ia3y5_SaUXyEfgU')
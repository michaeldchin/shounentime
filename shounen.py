import os
from botmain.embeds import get_image_embed, get_top_embed, get_time_embed, get_reminder_embed, get_bait_embed
from botmain.dbsetup import people_increment, get_random_bait, clear_bait
from botmain.bait import parse_bait_message
from botmain.reminders import add_reminder, check_reminders, show_user_reminders, clear_reminders
from discord.ext import commands
import discord
from datetime import datetime
from botmain.utils import load_config

config = load_config()
activity = discord.Game(name=datetime.now())
bot = commands.Bot(command_prefix=config["prefixes"], activity=activity)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    bot.loop.create_task(check_reminders(bot))


@bot.command()
async def image(ctx):
    people_increment(ctx.author)
    await ctx.send(embed=get_image_embed())


@bot.command()
async def top(ctx):
    await ctx.send(embed=get_top_embed())


@bot.command()
async def time(ctx):
    people_increment(ctx.author)
    await ctx.send(embed=get_time_embed())


@bot.command()
async def bait(ctx):
    people_increment(ctx.author)
    title, description, url, message = get_random_bait()
    await ctx.send(content=message, embed=get_bait_embed(title, description, url))


@bot.command()
async def addbait(ctx):
    content = parse_bait_message(ctx)
    await ctx.send(embed=get_reminder_embed(content))


@bot.command()
async def clearbait(ctx):
    content = clear_bait()
    await ctx.send(embed=get_reminder_embed(content))


@bot.command()
async def reminder(ctx):
    content = add_reminder(ctx)
    await ctx.send(embed=get_reminder_embed(content))


@bot.command()
async def showreminders(ctx):
    content = show_user_reminders(ctx)
    await ctx.send(embed=get_reminder_embed(content))


@bot.command()
async def clearreminders(ctx):
    content = clear_reminders(ctx)
    await ctx.send(embed=get_reminder_embed(content))


bot.run(config["token"])

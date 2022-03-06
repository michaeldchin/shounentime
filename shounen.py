import os
from botmain.embeds import get_image_embed, get_top_embed, get_time_embed, get_default_embed, get_bait_embed
import botmain.dbsetup as dbsetup
from botmain.bait import parse_bait_message
from botmain.reminders import add_reminder, check_reminders, show_user_reminders, clear_reminders
import randomimages.images as images
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
async def image(ctx, quote_id=None, image_id=None):
    dbsetup.people_increment(ctx.author)
    quote, image_url = images.handle_image(ctx, quote_id, image_id)
    await ctx.send(embed=get_image_embed(quote, image_url))


@bot.command()
async def top(ctx):
    await ctx.send(embed=get_top_embed())


@bot.command()
async def time(ctx):
    dbsetup.people_increment(ctx.author)
    await ctx.send(embed=get_time_embed())


@bot.command()
async def bait(ctx):
    dbsetup.people_increment(ctx.author)
    title, description, url, message = dbsetup.get_random_bait()
    await ctx.send(content=message, embed=get_bait_embed(title, description, url))


@bot.command()
async def addbait(ctx):
    description = parse_bait_message(ctx)
    await ctx.send(embed=get_default_embed(description))


@bot.command()
async def clearbait(ctx):
    description = dbsetup.clear_bait()
    await ctx.send(embed=get_default_embed(description))


@bot.command()
async def reminder(ctx):
    description = add_reminder(ctx)
    await ctx.send(embed=get_default_embed(description))


@bot.command()
async def showreminders(ctx):
    description = show_user_reminders(ctx)
    await ctx.send(embed=get_default_embed(description))


@bot.command()
async def clearreminders(ctx):
    description = clear_reminders(ctx)
    await ctx.send(embed=get_default_embed(description))


bot.run(config["token"])

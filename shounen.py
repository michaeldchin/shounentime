import os
from botmain.embeds import get_image_embed, get_top_embed, get_time_embed, get_reminder_embed
from botmain.dbsetup import people_increment
from botmain.reminders import add_reminder, check_reminders
from discord.ext import commands


prefixes = ['shounen ', 'Shounen ']
if os.environ['DEV'] == 'true':
    prefixes = ['dev ']
bot = commands.Bot(command_prefix=prefixes)


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
async def reminder(ctx):
    content = add_reminder(ctx)
    await ctx.send(embed=get_reminder_embed(content))

bot.run(os.environ['BOT_TOKEN'])

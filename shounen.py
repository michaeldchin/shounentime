import os
from botmain.embeds import get_image_embed, get_top_embed, get_time_embed, get_reminder_embed
from botmain.dbsetup import people_increment, add_reminder
from discord.ext import commands


prefixes = ['shounen ', 'Shounen ']
if os.environ['DEV']:
    prefixes = ['dev ']
bot = commands.Bot(command_prefix=prefixes)


@bot.event
async def on_ready():
    c = bot.get_channel(600919318359703552)
    # await c.send('extra testing <@143423784555118592> This is a full block: @\u200beveryone')
    # await c.send('extra testing @ everyone @ here')
    # await c.send('extra testing @everyone @here')
    print('We have logged in as {0.user}'.format(bot))


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

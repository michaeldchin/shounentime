import os
from botmain.embeds import get_image_embed, get_top_embed, get_time_embed
from botmain.dbsetup import people_increment
from discord.ext import commands


prefixes = ['shounen ', 'Shounen ', '!s']
if os.environ['DEV']:
    prefixes = ['dev ']
bot = commands.Bot(command_prefix=prefixes)


@bot.event
async def on_ready():
    # c = bot.get_channel(600919318359703552)
    # await c.send('extra testing <@143423784555118592>')
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
async def remind(ctx):
    await ctx.send('wip')

bot.run(os.environ['BOT_TOKEN'])

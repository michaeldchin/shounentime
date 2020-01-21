import discord
import os
from randomimages.images import random_quote, random_img
from bot.save import people_increment, people_top
from discord.ext import commands


prefixes = ['shounen ', 'Shounen ', '!s']
bot = commands.Bot(command_prefix=prefixes)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def image(ctx):
    people_increment(ctx.author)
    e = discord.Embed(color=0x777777, description=random_quote())
    url = random_img()
    e.set_image(url=url[0])
    await ctx.send(embed=e)


@bot.command()
async def top(ctx):
    _top = people_top()
    e = discord.Embed(color=0x770077,
                      title=':trophy: Shounen Time Leaderboard')
    e.set_thumbnail(url='https://cdn.discordapp.com/emojis/576627772949266435.png')
    e.add_field(name='Top Shounen Times', value=str(_top))
    await ctx.send(embed=e)


@bot.command()
async def time(ctx):
    people_increment(ctx.author)
    e = discord.Embed(color=0x777777)
    e.set_image(url='https://cdn.discordapp.com/attachments/572464049179328532/572639933139779594/Shounen_Time.png')
    await ctx.send(embed=e)

@bot.command()
async def remind(ctx):
    await ctx.send('wip')

bot.run(os.environ['BOT_TOKEN'])


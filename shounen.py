import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='shounen ')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def time(ctx):
    await ctx.send('https://discordapp.com/channels/479486540591005706/600919318359703552/600920989299113984')

bot.run('MzA2MTE2MTkyNjUxNzA2MzY5.XS6v_w.F3wPucGR9ZLWmkUBLplCvIvTqJg')
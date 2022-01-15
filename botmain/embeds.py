import discord
from randomimages.images import random_quote, random_img
from botmain.dbsetup import people_top


def get_image_embed():
    e = discord.Embed(color=0x777777, description=random_quote())
    url = random_img()
    e.set_image(url=url[0])
    return e


def get_top_embed():
    _top = people_top()
    e = discord.Embed(color=0x770077,
                      title=':trophy: Shounen Time Leaderboard')
    e.set_thumbnail(url='https://cdn.discordapp.com/emojis/576627772949266435.png')
    e.add_field(name='Top Shounen Times', value=str(_top))
    return e


def get_time_embed():
    e = discord.Embed(color=0x777777)
    e.set_image(url='https://cdn.discordapp.com/attachments/572464049179328532/572639933139779594/Shounen_Time.png')
    return e


def get_reminder_embed(content):
    e = discord.Embed(color=0x007777)
    e.description = content
    return e


def get_bait_embed(name, series, url):
    series += '\nReact with any emoji to claim!'
    e = discord.Embed(color=0xff8800, title=name, description=series)
    e.set_image(url=url)
    return e
import discord
import os
import sqlite3
from randomimages.images import random_quote, random_img
from discord.ext import commands

#
# DB
#
conn = sqlite3.connect('people.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS people
             (id TEXT, 
             person_name TEXT, 
             count INTEGER DEFAULT 0, 
             time TEXT)''')


def people_top():
    results = list(c.execute('''SELECT person_name, count 
                       FROM people ORDER BY count desc'''))
    count = 1
    output = ''
    for row in results:
        row_string = f'{count}. **{row[0]}** - {row[1]}\n'
        count = count + 1
        output = output + row_string

    return output


def people_increment(user_id, name):
    exists = c.execute('SELECT count(*) FROM people where id = ?', (user_id,)).fetchone()
    if exists[0] == 0:
        print('adding' + str((user_id, name)))
        c.execute('INSERT INTO people (id, person_name, count) VALUES (?,?,?)', (user_id, name, 1))
    else:
        print('incrementing' + str((user_id, name)))
        c.execute('UPDATE people SET count = count + 1 where id = ?', (user_id,))
    conn.commit()

#
# Bot commands
#


prefixes = ['shounen ', 'Shounen ', '!s']
bot = commands.Bot(command_prefix=prefixes)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def image(ctx):
    e = discord.Embed(color=0x777777, description=random_quote())
    url = random_img()
    e.set_image(url=url[0])
    await ctx.send(embed=e)


@bot.command()
async def top(ctx):
    _top = people_top()
    e = discord.Embed(color=0x770077,
                      title=':trophy: Shounen Time Leaderboard',
                      description='These stats are **not** permanent and might be deleted')
    e.set_thumbnail(url='https://cdn.discordapp.com/emojis/576627772949266435.png')
    e.add_field(name='Top Shounen Times', value=str(_top))
    await ctx.send(embed=e)


@bot.command()
async def time(ctx):
    user_id = ctx.author.id
    user_name = ctx.author.name
    user_discrm = ctx.author.discriminator
    people_increment(user_id, user_name + '#' + user_discrm)
    e = discord.Embed(color=0x777777)
    e.set_image(url='https://cdn.discordapp.com/attachments/572464049179328532/572639933139779594/Shounen_Time.png')
    await ctx.send(embed=e)

bot.run(os.environ['BOT_TOKEN'])


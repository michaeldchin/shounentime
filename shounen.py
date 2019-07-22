import discord
import os
import sqlite3
import threading
from randomimages.images import random_quote, random_img
from bot.save import savefile, loadfile, autosave
from discord.ext import commands


#
# DB
#
# Load and connect to DB
s3_db_location = os.environ['S3_DB_FILE']
loadfile(s3_db_location)
conn = sqlite3.connect('people.db')

# Setup tables
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS people
             (id TEXT, 
             person_name TEXT, 
             count INTEGER DEFAULT 0, 
             time TEXT)''')

# Setup autosave
thread = threading.Thread(target=autosave, args=(s3_db_location, 3600))
thread.start()


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
    user_id = ctx.author.id
    user_name = ctx.author.name
    user_discrm = ctx.author.discriminator
    people_increment(user_id, user_name + '#' + user_discrm)
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
    user_id = ctx.author.id
    user_name = ctx.author.name
    user_discrm = ctx.author.discriminator
    people_increment(user_id, user_name + '#' + user_discrm)
    e = discord.Embed(color=0x777777)
    e.set_image(url='https://cdn.discordapp.com/attachments/572464049179328532/572639933139779594/Shounen_Time.png')
    await ctx.send(embed=e)

#
# ADMIN COMMANDS
#


@bot.command()
async def save(ctx):
    if ctx.author.id == 143423784555118592:
        await ctx.send('Saving DB')
        f = open('people.db', 'rb')
        savefile(s3_db_location, f)
        f.close()
        await ctx.send('Save complete.')
    else:
        await ctx.send('You are not authorized to use this command.')


@bot.command()
async def load(ctx):
    if ctx.author.id == 143423784555118592:
        await ctx.send('Loading DB')
        loadfile(s3_db_location)
        await ctx.send('Load complete.')
    else:
        await ctx.send('You are not authorized to use this command.')

bot.run(os.environ['BOT_TOKEN'])


import discord, os, sqlite3
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
    _top = c.execute('''SELECT name, count 
                       FROM people ORDER BY count desc''')

    return [row.person_name + ': ' + row.shounen_count for row in _top]


def people_increment(_id, name):
    if c.execute('SELECT count(*) FROM people where id = ?', [_id]):
        c.execute('INSERT INTO people VALUES (?,?)', (_id, name))
    else:
        c.execute('UPDATE people SET count = count + 1 where id = ?', [name])

#
# Bot commands
#
bot = commands.Bot(command_prefix='shounen ')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def image(ctx):
    await ctx.send('pong')


@bot.command()
async def top(ctx):
    _top = people_top()
    e = discord.Embed(color=0x770077, title=':trophy: Shounen Time Leaderboard')
    e.set_thumbnail(url='https://cdn.discordapp.com/emojis/576627772949266435.png')
    e.add_field(name='these guys', value=str(_top))
    await ctx.send(embed=e)


@bot.command()
async def time(ctx):
    people_increment(ctx)
    e = discord.Embed(color=0x777777)
    e.set_image(url='https://cdn.discordapp.com/attachments/572464049179328532/572639933139779594/Shounen_Time.png')
    await ctx.send(embed=e)

bot.run(os.environ['BOT_TOKEN'])

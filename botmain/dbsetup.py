
import sqlite3
import re
from botmain.utils import clean_everyhere
conn = sqlite3.connect('people.db')

# Setup tables
c = conn.cursor()

peopleSql = '''
CREATE TABLE IF NOT EXISTS 
people (
    id TEXT, 
    person_name TEXT, 
    COUNT INTEGER DEFAULT 0, 
    time TEXT
)
'''
remindersSql = '''
CREATE TABLE IF NOT EXISTS 
reminders (
    discord_id TEXT, 
    reminder_time TIMESTAMP, 
    status TEXT DEFAULT 'pending', 
    channel TEXT,
    reminder_message TEXT
)
'''
c.execute(peopleSql)
# c.execute('DROP TABLE reminders')
c.execute(remindersSql)
# res = c.execute("select * from reminders")
# res
conn.commit()


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


def people_increment(author):
    user_id = author.id
    user_name = author.name + '#' + author.discriminator
    _people_increment(user_id, user_name)


def _people_increment(user_id, name):
    exists = c.execute('SELECT count(*) FROM people where id = ?', (user_id,)).fetchone()
    if exists[0] == 0:
        print('adding' + str((user_id, name)))
        c.execute('INSERT INTO people (id, person_name, count) VALUES (?,?,?)', (user_id, name, 1))
    else:
        print('incrementing' + str((user_id, name)))
        c.execute('UPDATE people SET count = count + 1 where id = ?', (user_id,))
    conn.commit()


def add_reminder(ctx):
    m = reminder_parse(ctx)
    return m


def reminder_parse(ctx):
    content = ctx.message.content
    reminder = re.split(r'^.*?remind (.*$)', content)[1]

    user_id = ctx.author.id
    time = 0

    _add_reminder(user_id,
                  time,
                  ctx.channel.id,
                  clean_everyhere(reminder))
    reminder_syntax_tip = 'Syntax: "remind (me|@user) (some reminder) (in|at) (time)"'
    response = 'Reminder set.' if True else reminder_syntax_tip
    return response


def _add_reminder(user_id, time, channel_id, reminder_message):
    sql = '''
        INSERT INTO reminders (
            discord_id,
            reminder_time,
            channel,
            reminder_message) VALUES (?,datetime(?),?,?)'''

    c.execute(sql, (user_id, time, channel_id, reminder_message))
    conn.commit()

import sqlite3
import re
import time
import pytz
import dateparser
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
    reminder_time INTEGER, 
    status TEXT DEFAULT 'pending', 
    channel TEXT,
    reminder_message TEXT
)
'''
c.execute(peopleSql)
# c.execute('DROP TABLE reminders')
c.execute(remindersSql)
res = c.execute("select * from reminders")
res
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
    captured = re.split(r'^.*?reminder (.*) (at .*$|in .*$)', content)
    if len(captured) > 2:
        reminder = captured[1]
        timestring = captured[2]
        date = _get_reminder_date(timestring)
        if date.timestamp() < time.time():
            return f"You're too late. Provided time {date.strftime('%m/%d/%Y, %H:%M:%S')} has already passed."
        else:
            timestamp = date.timestamp()
            user_id = ctx.author.id
            clean_reminder = clean_everyhere(reminder)
            _add_reminder(user_id,
                          timestamp,
                          ctx.channel.id,
                          clean_reminder)

            response = f"You will be reminded {clean_reminder} at {date.strftime('%m/%d/%Y, %H:%M:%S')}"
            return response
    else:
        reminder_syntax_tip = 'Syntax: "reminder (some reminder) (in|at) (time)"'
        return reminder_syntax_tip


def _is_utc(date):
    return date.utcoffset().total_seconds() == 0


def _get_reminder_date(timestring):
    date = dateparser.parse(timestring, settings={'RETURN_AS_TIMEZONE_AWARE': True})
    # set timezone to CST by default unless explicitly stated to be UTC
    if 'UTC' not in timestring.upper() and _is_utc(date):
        date = date.astimezone(pytz.timezone('US/Central'))
    return date


def _add_reminder(user_id, time, channel_id, reminder_message):
    sql = '''
        INSERT INTO reminders (
            discord_id,
            reminder_time,
            channel,
            reminder_message) VALUES (?,?,?,?)'''

    c.execute(sql, (user_id, time, channel_id, reminder_message))
    conn.commit()

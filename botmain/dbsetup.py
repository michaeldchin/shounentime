import sqlite3
import time
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
    discord_id INTEGER, 
    reminder_time INTEGER, 
    status TEXT DEFAULT 'pending', 
    channel INTEGER,
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


def insert_reminder(user_id, reminder_time, channel_id, reminder_message):
    sql = '''
        INSERT INTO reminders (
            discord_id,
            reminder_time,
            channel,
            reminder_message) VALUES (?,?,?,?)'''

    c.execute(sql, (user_id, reminder_time, channel_id, reminder_message))
    conn.commit()


def query_reminders():
    current_time = time.time()
    select_query = '''
        SELECT
            discord_id,   
            channel,  
            reminder_message
        FROM reminders 
        WHERE status = 'pending' AND reminder_time < ?
        '''
    res = c.execute(select_query, (current_time,)).fetchall()

    delete_query = '''
        DELETE FROM reminders 
        WHERE status = 'pending' AND reminder_time < ?
    '''
    c.execute(delete_query, (current_time,))

    conn.commit()
    return res


def query_user_reminders(user_id):
    select_query = '''
        SELECT
            reminder_time,
            reminder_message
        FROM reminders
        WHERE status = 'pending' AND discord_id = ?
        '''
    res = c.execute(select_query, (user_id,)).fetchall()
    return res


def clear_user_reminders(user_id):
    delete_query = '''
        DELETE FROM reminders 
        WHERE discord_id = ?
        '''
    res = c.execute(delete_query, (user_id,)).fetchall()
    conn.commit()
    return res

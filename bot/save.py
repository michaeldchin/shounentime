import boto3
import os
import time
import sqlite3
import threading

ACCESS_ID = os.environ['AWS_ACCESS_KEY_ID']
ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
BUCKET = 'shounen-bot-mdc'
s3_db_location = os.environ['S3_DB_FILE']

s3 = boto3.client('s3',
                  aws_access_key_id=ACCESS_ID,
                  aws_secret_access_key=ACCESS_KEY)


def loadfile():
    location = s3_db_location
    obj = s3.get_object(Bucket=BUCKET,
                        Key=location)
    data = obj['Body'].read()
    filename = location.split('/').pop()
    f = open(filename, 'wb')
    f.write(data)
    f.close()
    print(f'Loaded {location}')


def savefile(location, file):
    s3.put_object(Bucket=BUCKET,
                  Key=location,
                  Body=file)


def autosave(location, interval):
    while True:
        f = open('people.db', 'rb')
        savefile(location, f)
        f.close()
        print('Autosaving.')
        time.sleep(interval)

#
# DB
#
# Load and connect to DB
loadfile()
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
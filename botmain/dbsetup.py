from sqlalchemy import create_engine,  Column, Integer, String, Text, Date, select, insert, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func, select

import time
import datetime

engine = create_engine('sqlite+pysqlite:///people.db')
Base = declarative_base()

# Setup tables
class People(Base):
    __tablename__ = 'people'
    id = Column(Text, primary_key=True)
    person_name = Column(Text)
    count = Column(Integer, default=0)

class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_id = Column(Integer)
    reminder_time = Column(Integer)
    status = Column(Text, default='pending')
    channel = Column(Integer)
    reminder_message = Column(Text)

class Bait(Base):
    __tablename__ = 'bait'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, default='Title')
    description = Column(String, default='Description')
    url = Column(String, default='https://cdn.discordapp.com/attachments/572464049179328532/572639933139779594/Shounen_Time.png')
    message = Column(String)

class Quote(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quote = Column(Text, unique=True)
    author = Column(Text)
    guild_id = Column(Integer, default=None)
    created_at = Column(Date, default=datetime.datetime.now())

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True)
    guild_id = Column(Integer, default=None)
    created_at = Column(Date, default=datetime.datetime.now())


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind = engine)
session = Session()

### People ###
def people_top():
    stmt = select(People.person_name, People.count).order_by(People.count.desc())
    results = list(session.execute(stmt).all())
    output = ''
    for rank, row in enumerate(results):
        row_string = f'{rank+1}. **{row[0]}** - {row[1]}\n'
        output = output + row_string
    return output


def people_increment(author):
    user_id = author.id
    user_name = author.name + '#' + author.discriminator
    _people_increment(user_id, user_name)


def _people_increment(user_id, name):
    person = session.query(People).filter(People.id == user_id).first()
    if (person):
        person.count += 1
    else:
        session.add(People(id=user_id, person_name=name, count=1))
    session.commit()

### Reminders ###
def insert_reminder(user_id, reminder_time, channel_id, reminder_message):
    session.add(Reminder(
        discord_id=user_id, 
        reminder_time=reminder_time, 
        channel=channel_id, 
        reminder_message=reminder_message))
    session.commit()


def query_reminders():
    current_time = time.time()
    due_reminders = session.query(
            Reminder.discord_id, 
            Reminder.channel, 
            Reminder.reminder_message) \
        .filter(Reminder.reminder_time <= current_time) \
        .filter(Reminder.status == 'pending').all()

    session.query(Reminder).filter(Reminder.status == 'pending').filter(Reminder.reminder_time <= current_time).delete()
    session.commit()
    return due_reminders


def query_user_reminders(user_id):
    reminders = session.query(Reminder.reminder_time, Reminder.reminder_message) \
        .filter(Reminder.discord_id == user_id).all()
    return reminders


def clear_user_reminders(user_id):
    session.query(Reminder).filter(Reminder.discord_id == user_id).delete()
    session.commit()


### Bait ###
def get_random_bait():
    bait = session.query(
        Bait.title,
        Bait.description,
        Bait.url,
        Bait.message) \
        .order_by(func.random()).first()
    print(bait)
    return bait


def add_bait(title, description, url, message):
    session.add(Bait(title=title, description=description, url=url, message=message))
    session.commit()
    return 'Bait added!'

def clear_bait():
    session.query(Bait).delete()
    session.commit()
    return 'Bait cleared!'


### Quotes ###
def add_quote(quote, author, guild_id=None):
    if guild_id:
        session.add(Quote(quote=quote, author=author, guild_id=guild_id))
    else:
        session.add(Quote(quote=quote, author=author))
    session.commit()
    return 'quote added!'

def get_quote(id=None, guild_id=None):
    if id: 
        quote = session.query(Quote.quote, Quote.author) \
            .filter((Quote.guild_id == None) | (Quote.guild_id == guild_id)) \
            .filter(Quote.id == id).first()
    else:
        quote = session.query(Quote.quote, Quote.author) \
            .order_by(func.random()).first()
    return quote


### Images ###
def add_image(url, guild_id=None):
    if guild_id:
        session.add(Image(url=url, guild_id=guild_id))
    else:
        session.add(Image(url=url))
    session.commit()
    return 'Image added!'

def get_image(id=None, guild_id=None):
    if id: 
        url = session.query(Image.url) \
            .filter((Image.guild_id == None) | (Image.guild_id == guild_id)) \
            .filter(Image.id == id).first()
    else:
        url = session.query(Image.url) \
            .filter((Image.guild_id == None) | (Image.guild_id == guild_id)) \
            .order_by(func.random()).first()
    return url
from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, select, insert, update
from sqlalchemy.orm import registry, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import time

engine = create_engine('sqlite+pysqlite:///people.db', echo=True)

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

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind = engine)
session = Session()

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

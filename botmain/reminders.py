import re
import dateparser
from datetime import datetime
from botmain.utils import clean_everyhere
from botmain.dbsetup import insert_reminder, query_reminders, query_user_reminders, clear_user_reminders
import time
import asyncio

_DATE_FORMAT = '%m/%d/%Y, %I:%M:%S%p %Z'
_SLEEP_INTERVAL_SECONDS = 8


async def send_reminders(bot, data):

    async def send_reminder(datum):
        discord_id = datum[0]
        channel_id = datum[1]
        reminder_msg = datum[2]
        c = bot.get_channel(channel_id)
        await c.send(f'Reminder for <@{discord_id}> - {reminder_msg}')
    for x in data:
        await send_reminder(x)


async def check_reminders(bot):
    while True:
        res = query_reminders()
        await send_reminders(bot, res)
        await asyncio.sleep(_SLEEP_INTERVAL_SECONDS)


def add_reminder(ctx):
    m = reminder_parse(ctx)
    return m


def process_reminder(ctx, reminder, time_string):
    date = _get_reminder_date(time_string)
    timestamp = date.timestamp()
    if timestamp < time.time():
        return f"You're too late. Provided time {date.strftime(_DATE_FORMAT)} has already passed."
    else:
        user_id = ctx.author.id
        clean_reminder = clean_everyhere(reminder)
        insert_reminder(user_id,
                        timestamp,
                        ctx.channel.id,
                        clean_reminder)

        response = f"You will be reminded '{clean_reminder}' at {date.strftime(_DATE_FORMAT)}"
        return response


def show_user_reminders(ctx):
    user_id = ctx.author.id
    data = query_user_reminders(user_id)
    if len(data) == 0:
        return 'No upcoming reminders for this user.'
    output = 'Reminders: \n'
    for datum in data:
        timestamp = datum[0]
        message = datum[1]
        datestring = datetime.fromtimestamp(timestamp).strftime(_DATE_FORMAT)
        output += f"{message} at {datestring}\n"
    return output


def clear_reminders(ctx):
    user_id = ctx.author.id
    clear_user_reminders(user_id)
    return 'Reminders cleared.'


def reminder_parse(ctx):
    content = ctx.message.content
    captured = re.split(r'^.*?reminder (.*) (at .*$|in .*$)', content)
    reminder = captured[1]
    time_string = captured[2]
    if len(captured) > 2:
        return process_reminder(ctx, reminder, time_string)
    else:
        reminder_syntax_tip = '''
        **Failed to set reminder.**
        Syntax: "reminder (some reminder) (in|at) (date|time)"
        '''
        return reminder_syntax_tip


def _is_utc(date):
    return date.utcoffset().total_seconds() == 0


def _get_reminder_date(timestring):
    return dateparser.parse(timestring, settings={'TIMEZONE': 'US/Central', 'RETURN_AS_TIMEZONE_AWARE': True})


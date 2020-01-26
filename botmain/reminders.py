import re
import dateparser
from botmain.utils import clean_everyhere
from botmain.dbsetup import insert_reminder
import time


def add_reminder(ctx):
    m = reminder_parse(ctx)
    return m


def process_reminder(ctx, reminder, time_string):
    date = _get_reminder_date(time_string)
    timestamp = date.timestamp()
    if timestamp < time.time():
        return f"You're too late. Provided time {date.strftime('%m/%d/%Y, %I:%M%p %Z')} has already passed."
    else:
        user_id = ctx.author.id
        clean_reminder = clean_everyhere(reminder)
        insert_reminder(user_id,
                        timestamp,
                        ctx.channel.id,
                        clean_reminder)

        response = f"You will be reminded '{clean_reminder}' at {date.strftime('%m/%d/%Y, %I:%M%p %Z')}"
        return response


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
        Syntax: "reminder (some reminder) (in|at) (time)"
        '''
        return reminder_syntax_tip


def _is_utc(date):
    return date.utcoffset().total_seconds() == 0


def _get_reminder_date(timestring):
    date = dateparser.parse(timestring, settings={'TIMEZONE': 'CST', 'RETURN_AS_TIMEZONE_AWARE': True})
    return date
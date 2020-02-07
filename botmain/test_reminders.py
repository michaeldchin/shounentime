from botmain.reminders import *
from unittest.mock import patch, MagicMock
import unittest


class TestReminders(unittest.TestCase):

    def test_process_reminder(self):
        ctx = MagicMock()
        ctx.author.id = 1111
        ctx.channel.id = 3333
        reminder = 'to ask @everyone @micoolman'
        time_string = 'at 12pm'
        with patch('dbsetup.sqlite3') as mocksql:
            mocksql.connect().cursor().execute.return_value = ['John', 'Bob']
            result = process_reminder(ctx, reminder, time_string)
            expected = "You will be reminded 'to ask @​everyone @micoolman' at 02/07/2020, 12:00PM CST"
            self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

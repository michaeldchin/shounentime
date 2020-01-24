import re


def clean_everyhere(message):
    a = re.sub('@everyone', '@\u200beveryone', message)
    b = re.sub('@here', '@\u200bhere', a)
    return b

import json
import re

def clean_everyhere(message):
    a = re.sub('@everyone', '@\u200beveryone', message)
    b = re.sub('@here', '@\u200bhere', a)
    return b


def load_config(filename: str = "config"):
    """ Fetch default config file """
    try:
        with open(f"{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")
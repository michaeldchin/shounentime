import random
import csv


with open('randomimages/quotes.csv', 'r') as f:
    reader = csv.reader(f)
    quotes = list(reader)


with open('randomimages/images.csv', 'r') as f:
    reader = csv.reader(f)
    images = list(reader)


def _format_quote(quote_list):
    quote = quote_list[0]
    author = quote_list[1]
    return f"« {quote} » {author}"


def random_quote():
    rand_num = random.randint(0, len(quotes) - 1)
    return _format_quote(quotes[rand_num])


def random_img():
    rand_num = random.randint(0, len(images) - 1)
    return images[rand_num]


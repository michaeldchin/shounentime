import csv
import botmain.dbsetup as dbsetup

if (not dbsetup.get_image()):
    print('first time load image')
    with open('randomimages/images.csv', 'r') as f:
        reader = csv.reader(f)
        images = list(reader)
        for image in images:
            dbsetup.add_image(image[0])
else:
    print('loaded images')

if (not dbsetup.get_quote()):
    print('first time load quotes')
    with open('randomimages/quotes.csv', 'r') as f:
        reader = csv.reader(f)
        quotes = list(reader)
        for quote in quotes:
            dbsetup.add_quote(quote[0],quote[1])
else: 
    print('loaded quotes')


def _format_quote(quote_list):
    if not quote_list:
        return ''
    quote = quote_list[0]
    author = quote_list[1]
    return f"« {quote} » {author}"


def handle_image(ctx, quote_id, image_id):
    if quote_id == 'random':
        quoteData = dbsetup.get_quote(guild_id=ctx.guild.id)
    else:
        quoteData = dbsetup.get_quote(quote_id, guild_id=ctx.guild.id)
    quote = _format_quote(quoteData)

    image_result = dbsetup.get_image(image_id, guild_id=ctx.guild.id)
    if not image_result:
        image_url = 'https://i.kym-cdn.com/photos/images/original/002/113/379/aee.jpeg'
    else:
        image_url = image_result[0]

    return quote, image_url

def add_image(ctx, url):
    return dbsetup.add_image(url, guild_id=ctx.guild.id)

def add_quote(ctx, quote, author=''):
    return dbsetup.add_quote(quote, author, guild_id=ctx.guild.id)
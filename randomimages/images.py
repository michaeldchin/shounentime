import csv
import botmain.dbsetup as dbsetup


with open('randomimages/images.csv', 'r') as f:
    reader = csv.reader(f)
    images = list(reader)


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

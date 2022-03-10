import botmain.dbsetup as dbsetup

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

    if image_id == 'random':
        image_result = dbsetup.get_guild_image(guild_id=ctx.guild.id)
    else:
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

def show_custom(ctx):
    image_list = dbsetup.list_images(guild_id=ctx.guild.id)
    result = ''
    for entry in image_list:
        result += f"{entry[0]}: {entry[1]}\n"
    return result
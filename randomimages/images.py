import botmain.dbsetup as dbsetup

def _format_quote(quote_list):
    if not quote_list:
        return ''
    quote = quote_list[0]
    author = quote_list[1] if quote_list[1] else ''
    return f"« {quote} » {author}"


def handle_image(ctx, quote_id, image_id):
    if quote_id is not None and quote_id.lower() == 'random':
        quoteData = dbsetup.get_quote(guild_id=ctx.guild.id)
    else:
        quoteData = dbsetup.get_quote(quote_id, guild_id=ctx.guild.id)
    quote = _format_quote(quoteData)

    if image_id is not None and image_id.lower() == 'custom':
        image_result = dbsetup.get_guild_image(guild_id=ctx.guild.id)
    else:
        image_result = dbsetup.get_image(image_id, guild_id=ctx.guild.id)

    if not image_result:
        image_url = 'https://i.kym-cdn.com/photos/images/original/002/113/379/aee.jpeg'
    else:
        image_url = image_result[0]

    return quote, image_url

def add_image(ctx, url, flag):
    if flag == 'global':
        guild_id = None
    else:
        guild_id = ctx.guild.id
    return dbsetup.add_image(url, guild_id)

def add_quote(ctx, quote, author, flag):
    if flag == 'global':
        guild_id = None
    else:
        guild_id = ctx.guild.id
    return dbsetup.add_quote(quote, author, guild_id)

def show_custom(ctx):
    image_list = dbsetup.list_images(guild_id=ctx.guild.id)
    result = ''
    for entry in image_list:
        result += f"{entry[0]}: {entry[1]}\n"
    return result
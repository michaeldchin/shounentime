from os import error
from botmain.dbsetup import add_bait

def parse_bait_message(ctx):
    
    split = ctx.message.content.replace('shounen addbait ','').split('$')

    error = '**Invalid bait message.**\n' + ctx.message.content \
            + '\n' + 'Syntax: "shounen addbait (name) (description) (url) (description:optional)"'

    if (len(split) < 3):
        return error

    title = split[0]
    description = split[1]
    url = split[2]
    message = None
    if (len(split) > 3):
        message = f'Wished by <@{split[3]}>' 

    if (not url.startswith('http')):
        return error

    add_bait(title, description, url, message)
    return 'Bait added!'
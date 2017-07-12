import json

def get_resource(cwd, path):
    handle = open('%s/resources/%s' % (cwd, path), 'r')
    temp = handle.read()
    handle.close()

    return temp

def get_permissions(path, uID):
    temp = dict()

    with open(path, 'r') as f:
        temp = json.load(f).get(uID, dict())
    return temp

def split_nospace(str, prefix):
    temp = list(filter(None, str.split(prefix)))
    for s in temp:
        s.strip()
    return temp

async def syntax_output(instance, message_object, command, syntax_message):
    await instance.send_message(message_object.channel, 'Syntax: %s%s %s' % (instance.prefix, command, syntax_message))

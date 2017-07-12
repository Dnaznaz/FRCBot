def on_load(bot):
    pass

def assign_permissions():
    pass

async def on_message(instance, command, args, message_object):
    if not command == 'register':
        return False

    return True
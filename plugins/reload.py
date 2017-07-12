from utils import get_resource, get_permissions

async def on_message(instance, command, args, message_object):
    if not command == 'reload':
        return False

    perm = get_permissions(instance.cwd+'/resources/permissions', message_object.author.id)

    if perm.get('main',0) > 1 or perm.get('plugins', 0) > 0:
        await instance.send_message(message_object.channel, 'Reloading plugins')
        await instance.plugin_manager.reload_plugins()
    else:
        await instance.send_message(message_object.channel, '<@{id}> You are not authorized to reload the plugins'.format(
            id=message_object.author.id))

    return True

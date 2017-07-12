import json
from utils import get_permissions, split_nospace

async def assign_permissions(instance, message_object, uID, *permissions):
    if get_permissions(instance.cwd+'/resources/permissions', message_object.author.id)['main'] < 3:
        await instance.send_message(message_object.channel, '<@{id}> You are not authorized to give permissions'.format(
            id=message_object.author.id))
        return

    pArgs = []
    for permission in permissions:
        tempArgs = split_nospace(permission, '=')
        if len(tempArgs) != 2:
            return
        try:
            tempArgs[1] = int(tempArgs[1])
        except ValueError:
            return
        pArgs.append((tempArgs[0], tempArgs[1]))

    with open(instance.cwd+'/resources/permissions') as f:
        temp = json.load(f)

    for key, value in pArgs:
        temp[uID][key] = value

    with open(instance.cwd+'/resources/permissions', 'w') as f:
        json.dump(temp, f)

    await instance.send_message(message_object.channel, "The user <@{id}> was give the permissions '{permissions}'".format(
        id = uID,
        permissions = ', '.join(permissions)))

async def list_permissions(instance, message_object, uID, *permissions):
    rawPerms = get_permissions(instance.cwd+'/resources/permissions', uID)
    if len(permissions) > 0:
        temp = rawPerms.copy()
        for perm in temp:
            if perm not in permissions:
                rawPerms.pop(perm)

    if len(rawPerms) == 0:
        await instance.send_message(message_object.channel, "The user <@{id}> has non of the requested permissions".format(
        id = uID))
    return

    permissions = list(map(lambda x: '{}={}'.format(x[0], x[1]), rawPerms.items()))

    await instance.send_message(message_object.channel, "The user <@{id}> has the permissions:\n*{permissions}".format(
        id = uID,
        permissions = '\n*'.join(permissions)))

async def on_message(instance, command, args, message_object):
    if not command == 'access':
        return False

    if args is None:
        return True

    args = split_nospace(args, ' ')

    if args[0] == 'set' and len(args) > 2:
        await assign_permissions(instance, message_object, args[1][2:-1], *args[2:])
    elif args[0] == 'list' and len(args) > 1:
        await list_permissions(instance, message_object, args[1][2:-1], *args[2:])

    return True
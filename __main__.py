from bot import Bot
from utils import get_resource
from os import path

cwd = path.dirname(path.realpath(__file__))
bot_token = get_resource(cwd, 'token')

with Bot('\\', bot_token, cwd) as bot_instance:
    @bot_instance.event
    async def on_ready():
        print("Bot Operational, running under the name '{user}' on the approved servers.".format(
            user=bot_instance.user.name))


    bot_instance.run_bot()

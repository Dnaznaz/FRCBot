from discord import Client, errors
from asyncio import coroutine
from aiohttp import ClientSession
from plugin_manager import PluginManager
from utils import get_resource, split_nospace


class Bot(Client):
    def __init__(self, prefix, token, cwd):
        Client.__init__(self)
        self.prefix = prefix
        self.token = token
        self.cwd = cwd

        self.plugin_manager = PluginManager(self, '%s/plugins' % self.cwd)
        self.plugin_manager.load_plugins()

        user_agent = get_resource(self.cwd, 'user_agent')
        self.client_session = ClientSession(headers={'User-Agent': user_agent})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.plugin_manager.unload_plugins()
        self.client_session.close()
        self.close()

    @coroutine
    async def on_message(self, message_object):
        message = split_nospace(message_object.content, ' ')

        if not message or len(message[0]) < 2:
            return

        if not message[0][0] == self.prefix:
            return

        command = message[0][1:]
        arguments = None

        if len(message) > 1:
            arguments = ' '.join(message[1:])

        return_value = await self.plugin_manager.execute_message(command, arguments, message_object)

        if return_value:
            try:
                await self.delete_message(message_object)
            except errors.NotFound:
                pass

    def run_bot(self):
        self.run(self.token)

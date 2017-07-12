from importlib import import_module, reload
from asyncio import coroutine, get_event_loop
from os import listdir
from sys import modules


class PluginManager:
    def __init__(self, instance, cwd):
        self.instance = instance
        self.cwd = cwd
        self.plugins = []

    def load_plugins(self):
        for module in [module for module in listdir(self.cwd) if '.py' in module and '__' not in module]:
            try:
                self.plugins.append(import_module('plugins.%s' % module.replace('.py', '')))
            except Exception as e:
                print("[Plugin Manager] Failure to load (%s), skipping." % module)
                print("    >> %s" % e)

        self.execute_event('on_load')

        get_event_loop().run_until_complete(self._load_plugins())

        print("[Plugin Manager] Successfully loaded [%d / %d] plugins." % (
            len(self.plugins), len([module for module in listdir(self.cwd) if
                                    '.py' in module and '__' not in module])))

    def unload_plugins(self):
        self.execute_event('on_unload')

        for module in [module for module in modules.keys() if "plugins." in module]:
            del modules[module]

    @coroutine
    async def _load_plugins(self):
        await self._execute_event('_on_load')

    @coroutine
    async def reload_plugins(self):
        self.execute_event('on_unload')

        for module in [module for module in listdir(self.cwd) if '.py' in module and '__' not in module]:
            module_name = 'plugins.%s' % module.replace('.py', '')

            if module_name in modules.keys():
                current_module = modules[module_name]
                reload(current_module)
            else:
                self.plugins.append(import_module(module_name))

        self.execute_event('on_load')
        await self._load_plugins()

        print("[Plugin Manager] Successfully loaded [%d / %d] plugins." % (
            len(self.plugins), len([module for module in listdir(self.cwd) if
                                    '.py' in module and '__' not in module])))

    @coroutine
    async def _execute_event(self, event_name):
        for plugin in [plugin for plugin in self.plugins if hasattr(plugin, event_name)]:
            try:
                await getattr(plugin, event_name)(self.instance)
            except Exception as e:
                print("[Plugin Manager] Failure to execute async event in (%s), skipping." % plugin.__name__)
                print("    >> %s" % e)

    def execute_event(self, event_name):
        for plugin in [plugin for plugin in self.plugins if hasattr(plugin, event_name)]:
            try:
                getattr(plugin, event_name)(self.instance)
            except Exception as e:
                print("[Plugin Manager] Failure to execute event in (%s), skipping." % plugin.__name__)
                print("    >> %s" % e)

    def execute_module_event(self, module, event_name):
        if hasattr(module, event_name):
            try:
                getattr(module, event_name)(self.instance)
            except Exception as e:
                print("[Plugin Manager] Failure to execute module event in (%s), skipping." % module.__name__)
                print("    >> %s" % e)

    @coroutine
    async def execute_message(self, command, args, command_object):
        for plugin in [plugin for plugin in self.plugins if hasattr(plugin, 'on_message')]:
            try:
                value = await getattr(plugin, 'on_message')(self.instance, command, args, command_object)
                if value:
                    return True
            except Exception as e:
                print("[Plugin Manager] Failure to pass message to (%s), skipping." % plugin.__name__)
                print("    >> %s" % e)

        return False

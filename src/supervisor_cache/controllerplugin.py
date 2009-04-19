from supervisor.supervisorctl import ControllerPluginBase
import pprint

class CacheControllerPlugin(ControllerPluginBase):
    def __init__(self, controller):
        self.ctl   = controller     
        self.cache = controller.get_server_proxy('cache')

    def do_cache_keys(self, args):
        keys = self.cache.getKeys()
        self._pprint(keys)

    def do_cache_fetch(self, args):
        value = self.cache.fetch(args)
        self._pprint(value)

    def do_cache_store(self, args):
        splitted = args.split(None, 1)
        if len(splitted) != 2:
            self.help_cache_store()
            return
            
        key, value = splitted
        self.cache.store(key, value)        

    def do_cache_delete(self, args):
        value = self.cache.delete(args)

    def do_cache_clear(self, args):
        value = self.cache.clear()

    def _pprint(self, what):
        pprinted = pprint.pformat(what)
        self.ctl.output(pprinted)        


def make_cache_controllerplugin(supervisord, **config):
    return CacheControllerPlugin(supervisord)

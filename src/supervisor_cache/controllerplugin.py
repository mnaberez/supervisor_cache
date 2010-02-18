from supervisor.supervisorctl import ControllerPluginBase
import pprint
import shlex

class CacheControllerPlugin(ControllerPluginBase):
    def __init__(self, controller):
        self.ctl   = controller     
        self.cache = controller.get_server_proxy('cache')

    # cache_clear

    def do_cache_clear(self, args):
        if args:
            return self.help_cache_clear()
        self.cache.clear()

    def help_cache_clear(self):
        self.ctl.output("cache_clear\t"
                        "Clear all items from the cache.")

    # cache_count

    def do_cache_count(self, args):
        if args:
            return self.help_cache_count()
        count = self.cache.getCount()
        self.ctl.output(str(count))

    def help_cache_count(self):
        self.ctl.output("cache_count\t"
                        "Get a count of all items in the cache.")

    # cache_delete

    def do_cache_delete(self, args):
        splitted = shlex.split(args)
        if len(splitted) != 1:
            return self.help_cache_delete()
        key = splitted[0]
        self.cache.delete(key)

    def help_cache_delete(self):
        self.ctl.output("cache_delete <key>\t"
                        "Delete the item cached at <key>.")

    # cache_fetch

    def do_cache_fetch(self, args):
        splitted = shlex.split(args)
        if len(splitted) != 1:
            return self.help_cache_fetch()
        key = splitted[0]        
        value = self.cache.fetch(key)
        self._pprint(value)

    def help_cache_fetch(self):
        self.ctl.output("cache_fetch <key>\t"
                        "Fetch the item cached at <key>.")

    # cache_keys

    def do_cache_keys(self, args):
        if args:
            return self.help_cache_keys()
        keys = self.cache.getKeys()
        self._pprint(keys)

    def help_cache_keys(self):
        self.ctl.output("cache_keys\t"
                        "List the keys of all items in the cache.")

    # cache_store

    def do_cache_store(self, args):
        splitted = shlex.split(args)
        if len(splitted) != 2:
            return self.help_cache_store()
        key, value = splitted
        self.cache.store(key, value)        

    def help_cache_store(self): 
        self.ctl.output("cache_store <key> <value>\t"
                        "Store <value> in the cache at <key>.")


    def _pprint(self, what):
        pprinted = pprint.pformat(what)
        self.ctl.output(pprinted)        


def make_cache_controllerplugin(controller, **config):
    return CacheControllerPlugin(controller)

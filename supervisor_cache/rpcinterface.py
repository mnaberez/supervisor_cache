from supervisor.supervisord import SupervisorStates
from supervisor.xmlrpc import Faults
from supervisor.xmlrpc import RPCError

API_VERSION = '0.2'

class CacheNamespaceRPCInterface:
    """ A Supervisor RPC interface that provides the ability
    to cache abritrary data in the Supervisor instance as key/value pairs.
    """

    def __init__(self, supervisord):
        self.supervisord = supervisord
        self.cache = {}

    def _update(self, text):
        self.update_text = text # for unit tests, mainly

        state = self.supervisord.get_state()

        if state == SupervisorStates.SHUTDOWN:
            raise RPCError(Faults.SHUTDOWN_STATE)

        # XXX fatal state

    # RPC API methods

    def getAPIVersion(self):
        """ Return the version of the RPC API used by supervisor_cache

        @return string  version
        """
        self._update('getAPIVersion')
        return API_VERSION

    def getKeys(self):
        """ Return keys for all data stored in the cache

        @return  array   An array of strings representing cache keys
        """
        self._update('getKeys')
        return sorted(self.cache.keys())

    def getCount(self):
        """ Return a count of all items in the cache

        @return  integer   Count of items
        """
        self._update('getCount')
        return len(self.cache)

    def store(self, key, data):
        """ Store a string value in the cache, referenced by 'key'

        @param  string key   A string to use as a cache key
        @param  string data  A string for cache value
        @return boolean      Always true unless error
        """
        self._update('store')
        self._validateKey(key)

        if not isinstance(data, str):
            why = 'Cache data must be a string'
            raise RPCError(Faults.INCORRECT_PARAMETERS, why)

        self.cache[key] = data
        return True

    def fetch(self, key):
        """ Retrieve data from cache stored under 'key'

        @param  string key  The cache key
        @return string      Cache data stored at key
        """
        self._update('fetch')
        self._validateKey(key)

        data = self.cache.get(key)
        if data is None:
            raise RPCError(Faults.BAD_NAME)
        return data

    def delete(self, key):
        """ Delete data stored in cache under 'key'

        @param  string  key  The key to delete from the cache
        @return boolean      Always true unless error.
        """
        self._update('delete')
        self._validateKey(key)

        if key in self.cache:
            del self.cache[key]
        return True

    def clear(self):
        """ Clear the cache

        @return boolean  Always true unless error.
        """
        self._update('clear')
        self.cache.clear()
        return True

    def _validateKey(self, key):
        """ validate 'key' is suitable for a cache key name """
        if not isinstance(key, str) or (key == ''):
            why = 'Cache key must be a non-empty string'
            raise RPCError(Faults.BAD_NAME, why)

def make_cache_rpcinterface(supervisord, **config):
    return CacheNamespaceRPCInterface(supervisord)

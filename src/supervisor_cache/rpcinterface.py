import xmlrpclib

from supervisor.supervisord import SupervisorStates
from supervisor.xmlrpc import Faults as SupervisorFaults
from supervisor.xmlrpc import RPCError

API_VERSION = '1.0'

class CacheNamespaceRPCInterface:
    """ A supervisor rpc interface that provides the ability 
    to cache limited amounts of data in the supervisor instance 
    in key/value pairs.    
    """

    def __init__(self, supervisord):
        self.supervisord = supervisord
        self.cache = {}
        
    def _update(self, text):
        self.update_text = text # for unit tests, mainly

        state = self.supervisord.get_state()

        if state == SupervisorStates.SHUTDOWN:
            raise RPCError(SupervisorFaults.SHUTDOWN_STATE)

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
        
        return self.cache.keys()

    def store(self, key, data):
        """ Store a cache value in 'key'

        @param  string key   A string to use as a cache key
        @param  string data  A string for cache value (may also be Binary)
        @return boolean      Always true unless error
        """
        self._update('store')
        
        if isinstance(data, xmlrpclib.Binary):
            data = data.data

        try:
            key = str(key)
            if key == '':
                raise RPCError(SupervisorFaults.BAD_NAME)
            self.cache[key] = data
        except RPCError:
            raise
        except:
            raise RPCError(SupervisorFaults.FAILED)

        return True

    def fetch(self, key):
        """ Retrieve data from cache stored under 'key'

        @param  string key  The cache key
        @return binary      An xmlrpc Binary value
        """
        self._update('fetch')

        key = str(key)
        data = self.cache.get(key)
        if data is None:
            raise RPCError(SupervisorFaults.BAD_NAME)
        try:
            return xmlrpclib.Binary(data)
        except:
            raise RPCError(SupervisorFaults.FAILED)

    def delete(self, key):
        """ Delete data stored in cache under 'key'

        @param  string  key  The key to delete from the cache
        @return boolean      Always true unless error.
        """
        self._update('delete')

        if self.cache.has_key(key):
            del self.cache[key]
        return True

    def clear(self):
        """ Clear the cache

        @return boolean  Always true unless error.
        """
        self._update('clear')

        self.cache.clear()
        return True

def make_cache_rpcinterface(supervisord, **config):
    return CacheNamespaceRPCInterface(supervisord)

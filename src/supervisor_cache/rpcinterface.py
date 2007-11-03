import os

from supervisor.options import UnhosedConfigParser
from supervisor.options import ProcessGroupConfig
from supervisor.supervisord import SupervisorStates
from supervisor.xmlrpc import Faults as SupervisorFaults
from supervisor.xmlrpc import RPCError
from supervisor.http import NOT_DONE_YET

API_VERSION = '1.0'

class Faults:
    STILL_RUNNING = 220

class CacheNamespaceRPCInterface:
    """ A supervisor rpc interface for caching """

    def __init__(self, supervisord):
        self.supervisord = supervisord

    def _update(self, text):
        self.update_text = text # for unit tests, mainly

        state = self.supervisord.get_state()

        if state == SupervisorStates.SHUTDOWN:
            raise RPCError(SupervisorFaults.SHUTDOWN_STATE)

        # XXX fatal state
        
    # RPC API methods

    def getAPIVersion(self):
        """ Return the version of the RPC API used by supervisor_cache

        @return int version version id
        """
        self._update('getAPIVersion')
        return API_VERSION


def make_cache_rpcinterface(supervisord, **config):
    return CacheNamespaceRPCInterface(supervisord)

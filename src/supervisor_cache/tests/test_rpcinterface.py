import sys
import unittest
import xmlrpclib

import supervisor
from supervisor.xmlrpc import Faults as SupervisorFaults
from supervisor.supervisord import SupervisorStates

import supervisor_cache

from supervisor.tests.base import DummySupervisor
from supervisor.tests.base import DummyPConfig, DummyProcess
from supervisor.tests.base import DummyPGroupConfig, DummyProcessGroup

class TestRPCInterface(unittest.TestCase):

    # Constructor
    
    def test_ctor_assigns_supervisord(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)
    
        self.assertEqual(supervisord, interface.supervisord)

    # Factory
    
    def test_make_cache_rpcinterface_factory(self):
        from supervisor_cache import rpcinterface

        supervisord = DummySupervisor()
        interface = rpcinterface.make_cache_rpcinterface(supervisord)
        
        self.assertType(rpcinterface.CacheNamespaceRPCInterface, interface)
        self.assertEquals(supervisord, interface.supervisord)

    # Updater
    
    def test_updater_raises_shutdown_error_if_supervisord_in_shutdown_state(self):
        supervisord = DummySupervisor(state = SupervisorStates.SHUTDOWN)
        interface = self.makeOne(supervisord)
        
        self.assertRPCError(SupervisorFaults.SHUTDOWN_STATE, 
                            interface.getAPIVersion)
    
    # API Method cache.getAPIVersion()
    
    def test_getAPIVersion_returns_api_version(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)
    
        version = interface.getAPIVersion()
        self.assertEqual('getAPIVersion', interface.update_text)
    
        from supervisor_cache.rpcinterface import API_VERSION
        self.assertEqual(version, API_VERSION)

    # API Method cache.store()
    
    def test_store_raises_bad_name_when_key_is_invalid(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)

        self.assertRPCError(SupervisorFaults.BAD_NAME,
                    interface.store, '', 'data')
    
    def test_store(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)

        interface.store('the-key', 'its-value')
        self.assertEqual(interface.cache['the-key'], 'its-value')
        self.assertEqual(interface.update_text, 'store')
    
    def test_store_handles_binary_values(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)

        interface.store('the-key', xmlrpclib.Binary('its-binary-value'))
        self.assert_(not isinstance(interface.cache['the-key'], xmlrpclib.Binary))
        self.assertEqual(interface.cache['the-key'], 'its-binary-value')
    
    # API Method cache.getKeys()
    
    def test_getKeys_returns_empty_list_when_no_items_cache(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)
        interface.cache = {}

        self.assertEqual(interface.getKeys(), [])
        self.assertEqual(interface.update_text, 'getKeys')

    def test_getKeys_returns_list_of_keys_for_items_in_cache(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)
        interface.cache = {'foo': None, 'bar': None}

        self.assertEqual(interface.getKeys(), ['foo','bar'])
        self.assertEqual(interface.update_text, 'getKeys')
    
    # API Method cache.fetch()
    
    def test_fetch_raises_bad_name_when_key_does_not_exist(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)
        interface.cache = {}
                
        self.assertRPCError(SupervisorFaults.BAD_NAME, 
                            interface.fetch, 'nonexistant-key')
    
    def test_fetch(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)
        interface.cache = {'the-key': 'its-value'}

        self.assertEqual('its-value', interface.fetch('the-key'))
        self.assertEqual(interface.update_text, 'fetch')

    # API Method cache.delete()
    
    def test_delete_fails_silently_when_key_does_not_exist(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)
        interface.cache = {}

        self.assertTrue(interface.delete('nonexistant-key'))

    def test_delete_removes_data_from_cache_by_key(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)
        interface.cache = {'delete-me': 'foo', 'keep-me': 'bar'}

        self.assertTrue(interface.delete('delete-me'))
        self.assertEqual({'keep-me': 'bar'}, interface.cache)
    
    # API Method cache.clear()
    
    def test_clear(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)
        interface.cache = {'foo': 'bar'}
        
        interface.clear()
        self.assertEqual({}, interface.cache)
        self.assertEqual(interface.update_text, 'clear')

    # Helpers Methods
    
    def getTargetClass(self):
        from supervisor_cache.rpcinterface import CacheNamespaceRPCInterface
        return CacheNamespaceRPCInterface

    def makeOne(self, *arg, **kw):
        return self.getTargetClass()(*arg, **kw)

    def attrDictWithoutUnders(self, obj):
        """ Returns the __dict__ for an object with __unders__ removed """
        attrs = {}
        for k, v in obj.__dict__.items():
            if not k.startswith('__'): attrs[k] = v
        return attrs

    # Helper Assertion Methods

    def assertRPCError(self, code, callable, *args, **kw):
        try:
            callable(*args, **kw)
        except supervisor.xmlrpc.RPCError, inst:
            self.assertEqual(inst.code, code)
        else:
            fail('RPCError was never raised')

    def assertTrue(self, obj):
        self.assert_(obj is True)

    def assertFalse(self, obj):
        self.assert_(obj is False)
    
    def assertNone(self, obj):
        self.assert_(obj is None)

    def assertType(self, typeof, obj):
        self.assertEqual(True, isinstance(obj, typeof), 'type mismatch')


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

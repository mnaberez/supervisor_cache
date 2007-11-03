import sys
import unittest

import supervisor
from supervisor.xmlrpc import Faults as SupervisorFaults
from supervisor.supervisord import SupervisorStates

import supervisor_cache
from supervisor_cache.rpcinterface import Faults as CacheFaults

from supervisor.tests.base import DummySupervisor
from supervisor.tests.base import DummyPConfig, DummyProcess
from supervisor.tests.base import DummyPGroupConfig, DummyProcessGroup

class TestRPCInterface(unittest.TestCase):

    # Fault Constants

    def test_cache_fault_names_dont_clash_with_supervisord_fault_names(self):
        supervisor_faults = self.attrDictWithoutUnders(SupervisorFaults)
        cache_faults = self.attrDictWithoutUnders(CacheFaults)

        for name in supervisor_faults.keys():
            self.assertNone(cache_faults.get(name))

    def test_cache_fault_codes_dont_clash_with_supervisord_fault_codes(self):
        supervisor_fault_codes = self.attrDictWithoutUnders(SupervisorFaults).values()
        cache_fault_codes = self.attrDictWithoutUnders(CacheFaults).values()

        for code in supervisor_fault_codes:
            self.assertFalse(code in cache_fault_codes)

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

import sys
import unittest

import supervisor
from supervisor.xmlrpc import Faults
from supervisor.supervisord import SupervisorStates

from supervisor.tests.base import DummySupervisor

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

        self.assertTrue(isinstance(interface,
                                rpcinterface.CacheNamespaceRPCInterface))
        self.assertEqual(supervisord, interface.supervisord)

    # Updater

    def test_updater_raises_shutdown_error_if_supervisord_in_shutdown_state(self):
        supervisord = DummySupervisor(state = SupervisorStates.SHUTDOWN)
        interface = self.makeOne(supervisord)

        self.assertRPCError(Faults.SHUTDOWN_STATE,
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

    def test_store_raises_bad_name_when_key_is_not_a_string(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)

        not_a_string = 42
        self.assertRPCError(Faults.BAD_NAME,
                    interface.store, not_a_string, 'data')

    def test_store_raises_bad_name_when_key_is_an_empty_string(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)

        self.assertRPCError(Faults.BAD_NAME,
                    interface.store, '', 'data')

    def test_store_raises_incorrect_parameters_when_data_is_not_string(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)

        not_a_string = 42
        self.assertRPCError(Faults.INCORRECT_PARAMETERS,
                    interface.store, 'key', not_a_string)

    def test_store(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)

        interface.store('the-key', 'its-value')
        self.assertEqual(interface.cache['the-key'], 'its-value')
        self.assertEqual(interface.update_text, 'store')

    # API Method cache.getCount()

    def test_getCount(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)
        interface.cache = dict(foo='bar', baz='qux')
        self.assertEqual(2, interface.getCount())
        self.assertEqual(interface.update_text, 'getCount')

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

        self.assertEqual(interface.getKeys(), ['bar','foo'])
        self.assertEqual(interface.update_text, 'getKeys')

    # API Method cache.fetch()

    def test_fetch_raises_bad_name_when_key_is_not_a_string(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)

        not_a_string = 42
        self.assertRPCError(Faults.BAD_NAME,
                    interface.fetch, not_a_string)

    def test_fetch_raises_bad_name_when_key_is_an_empty_string(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)

        self.assertRPCError(Faults.BAD_NAME,
                    interface.fetch, '')

    def test_fetch_raises_bad_name_when_key_does_not_exist(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)
        interface.cache = {}

        self.assertRPCError(Faults.BAD_NAME,
                            interface.fetch, 'nonexistant-key')

    def test_fetch(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)
        interface.cache = {'the-key': 'its-value'}

        self.assertEqual('its-value', interface.fetch('the-key'))
        self.assertEqual(interface.update_text, 'fetch')

    # API Method cache.delete()

    def test_delete_raises_bad_name_when_key_is_not_a_string(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)

        not_a_string = 42
        self.assertRPCError(Faults.BAD_NAME,
                    interface.delete, not_a_string)

    def test_delete_raises_bad_name_when_key_is_an_empty_string(self):
        supervisord = DummySupervisor()
        interface = self.makeOne(supervisord)

        self.assertRPCError(Faults.BAD_NAME,
                    interface.delete, '')

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
        self.assertEqual(None, interface.cache.get('delete-me'))
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

    # Helper Assertion Methods

    def assertRPCError(self, code, callable, *args, **kw):
        try:
            callable(*args, **kw)
        except supervisor.xmlrpc.RPCError as e:
            self.assertEqual(e.code, code)
        else:
            self.fail('RPCError was never raised')


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

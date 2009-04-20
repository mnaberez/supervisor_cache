import sys
import unittest
import StringIO
import supervisor_cache

class TestControllerPlugin(unittest.TestCase):

    # Factory
    
    def test_make_cache_controllerplugin_factory(self):
        from supervisor_cache import controllerplugin
        controller = DummyController()
        plugin = controllerplugin.make_cache_controllerplugin(controller)
        self.assertEqual(controller, plugin.ctl)

    # Constructor
    
    def test_ctor_assigns_controller(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        self.assertEqual(controller, plugin.ctl)

    # cache_clear

    def test_do_cache_clear(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        cache_interface = plugin.cache
        cache_interface.cache = dict(foo='bar')        
        plugin.do_cache_clear('')
        self.assertEqual({}, cache_interface.cache)

    # cache_fetch
    
    def test_do_cache_fetch(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        cache_interface = plugin.cache
        cache_interface.cache = dict(foo='bar')
        plugin.do_cache_fetch('foo')
        
        output = controller.sio.getvalue()
        self.assertEqual("'bar'", output)
    
    # cache_store
    
    def test_do_cache_store(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        cache_interface = plugin.cache
        cache_interface.cache = {}
        plugin.do_cache_store('foo bar')
        self.assertEqual('bar', cache_interface.cache['foo'])

    # cache_delete
    
    def test_do_cache_delete(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        cache_interface = plugin.cache
        cache_interface.cache = dict(foo='bar', baz='qux')
        plugin.do_cache_delete('foo')
        
        self.assertEqual(None, cache_interface.cache.get('foo', None))  
        self.assertEqual('qux', cache_interface.cache['baz'])  

    # cache_keys
    
    def test_do_cache_keys(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        cache_interface = plugin.cache
        cache_interface.cache = dict(foo='bar', baz='qux')
        plugin.do_cache_keys('')
        
        output = controller.sio.getvalue()
        self.assert_('foo' in output)
        self.assert_('baz' in output)
        

    # Test Helpers

    def makeOne(self, *arg, **kw):
        return self.getTargetClass()(*arg, **kw)

    def getTargetClass(self):
        from supervisor_cache.controllerplugin import CacheControllerPlugin
        return CacheControllerPlugin


class DummyController:
    def __init__(self):
        self.sio = StringIO.StringIO()
    
    def output(self, out):
        self.sio.write(out)
            
    def get_server_proxy(self, namespace=None):
        if namespace == 'cache':
            from supervisor.tests.base import DummySupervisor
            supervisor = DummySupervisor()

            from supervisor_cache.rpcinterface import CacheNamespaceRPCInterface
            cache = CacheNamespaceRPCInterface(supervisor)

            return cache


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

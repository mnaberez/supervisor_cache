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

    def test_help_cache_clear(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        plugin.help_cache_clear()
        out = controller.sio.getvalue()
        self.assert_(out.startswith('cache_clear'))

    # cache_fetch
    
    def test_do_cache_fetch(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        cache_interface = plugin.cache
        cache_interface.cache = dict(foo='bar')
        plugin.do_cache_fetch('foo')
        
        output = controller.sio.getvalue()
        self.assertEqual("'bar'", output)

    def test_help_cache_fetch(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        plugin.help_cache_fetch()
        out = controller.sio.getvalue()
        self.assert_(out.startswith('cache_fetch <key>'))
   
    # cache_store
    
    def test_do_cache_store(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        cache_interface = plugin.cache
        cache_interface.cache = {}
        plugin.do_cache_store('foo bar')
        self.assertEqual('bar', cache_interface.cache['foo'])

    def test_help_cache_store(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        plugin.help_cache_store()
        out = controller.sio.getvalue()
        self.assert_(out.startswith('cache_store <key> <value>'))           

    # cache_delete
    
    def test_do_cache_delete(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        cache_interface = plugin.cache
        cache_interface.cache = dict(foo='bar', baz='qux')
        plugin.do_cache_delete('foo')
        
        self.assertEqual(None, cache_interface.cache.get('foo', None))  
        self.assertEqual('qux', cache_interface.cache['baz'])  

    def test_help_cache_delete(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        plugin.help_cache_delete()
        out = controller.sio.getvalue()
        self.assert_(out.startswith('cache_delete <key>'))           

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

    def test_help_cache_keys(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        plugin.help_cache_keys()
        out = controller.sio.getvalue()
        self.assert_(out.startswith('cache_keys'))           

    # cache_count
    
    def test_do_cache_count(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        cache_interface = plugin.cache
        cache_interface.cache = dict(foo='bar', baz='qux')
        plugin.do_cache_count('')
        
        output = controller.sio.getvalue()
        self.assertEqual('2', output)
   
    def test_help_cache_count(self):
        controller = DummyController()
        plugin = self.makeOne(controller)

        plugin.help_cache_count()
        out = controller.sio.getvalue()
        self.assert_(out.startswith('cache_count'))           

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
        assert(isinstance(out, str))
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

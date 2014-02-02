# supervisor_cache

This package is an extension for [Supervisor](http://supervisord.org)
that provides the ability to cache arbitrary data directly inside a
Supervisor instance as key/value pairs.

It also serves as a reference for how to write Supervisor extensions.

## Installation

Release packages are [available](http://pypi.python.org/pypi/supervisor_cache)
on the Python Package Index (PyPI).  You can download them from there or you
can use `easy_install` to automatically install or upgrade:

    $ easy_install -U supervisor_cache

Alternatively, you can [download](http://github.com/mnaberez/supervisor_cache/downloads)
a package from GitHub in `.tar.gz` or `.zip` format.  After extracting the
package, use the following command to install:

    $ python setup.py install

After installing the package, you must modify your `supervisord.conf` file
to register the RPC interface and `supervisorctl` plugin:

    [rpcinterface:cache]
    supervisor.rpcinterface_factory = supervisor_cache.rpcinterface:make_cache_rpcinterface

    [ctlplugin:cache]
    supervisor.ctl_factory = supervisor_cache.controllerplugin:make_cache_controllerplugin

After modifying the `supervisord.conf` file, both your `supervisord` instance and
`supervisorctl` must be restarted for these changes to take effect.

## XML-RPC

The cache functions allow key/value pairs to be stored and fetched over Supervisor's
XML-RPC interface. The following Python interpreter session demonstrates the usage.

First, a `ServerProxy` object must be configured.  If supervisord is listening on
an inet socket, `ServerProxy` configuration is simple:

    >>> import xmlrpclib
    >>> s = xmlrpclib.ServerProxy('http://localhost:9001')

If supervisord is listening on a domain socket, `ServerProxy` can be configured
with `SupervisorTransport`.  The URL must still be supplied and be a valid HTTP
URL to appease `ServerProxy`, but it is superfluous.

    >>> import xmlrpclib
    >>> from supervisor.xmlrpc import SupervisorTransport
    >>> s = xmlrpclib.ServerProxy('http://127.0.0.1/whatever',
    ... SupervisorTransport('', '', 'unix:///path/to/supervisor.sock'))

Once `ServerProxy` has been configured appropriately, we can now exercise
`supervisor_cache`:

    >>> s.cache.getKeys()
    []
    >>> s.cache.store('foo', 'bar baz')
    True
    >>> s.cache.fetch('foo')
    'bar baz'
    >>> s.cache.getKeys()
    ['foo']

The key must be a string and cannot be zero-length.  The value must also be a
string but is permitted to be zero-length.

Please consult the inline source documentation for the specifics of each
command available.

## Supervisorctl

You can also interact with the cache using `supervisorctl`.  The `help` command
with no arguments will list the available cache commands:

    supervisor> help
    ...

    cache commands (type help <topic>):
    ===================================
    cache_clear  cache_count  cache_delete  cache_fetch  cache_keys  cache_store

Each command provides a thin wrapper around an XML-RPC method:

    supervisor> cache_keys
    []
    supervisor> cache_store 'foo' 'bar baz'
    supervisor> cache_fetch 'foo'
    'bar baz'
    supervisor> cache_keys
    ['foo']

## Warnings

Data is not discarded from the cache until it is explicitly deleted with the
`cache.delete()` method.  Data does not persist after Supervisor is shut down.

Your Supervisor instance should never be exposed to the outside world.  It is
quite easy to perform a denial of service attack by filling `supervisor_cache`
with large amounts of data.

## Author

[Mike Naberezny](http://github.com/mnaberez)

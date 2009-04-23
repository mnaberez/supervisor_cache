# supervisor_cache

This package is an extension for [Supervisor](http://supervisord.org) 
that provides the ability to cache arbitrary data directly inside a 
Supervisor instance as key/value pairs.  

It also serves as a reference for how to write Supervisor extensions.

## Installation

[Download](http://github.com/mnaberez/supervisor_cache/downloads) and 
extract, then install to Python's `site-packages`:

    python setup.py install
    
After installing the package, you must modify your `supervisord.conf` file 
to register the RPC interface and `supervisorctl` plugin: 

    [rpcinterface:cache]
    supervisor.rpcinterface_factory = supervisor_cache.rpcinterface:make_cache_rpcinterface

    [ctlplugin:cache]
    supervisor.ctl_factory = supervisor_cache.controllerplugin:make_cache_controllerplugin

After modifying the `supervisord.conf` file, both your `supervisord` instance and 
`supervisorctl` must be restarted for these changes to take effect.

## Usage

The cache functions allow key/value pairs to be stored and fetched. The
following Python interpreter session demonstrates the usage.

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
    >>> s.cache.store('foo', 'bar')
    True
    >>> s.cache.fetch('foo')
    'bar'
    >>> s.cache.getKeys()
    ['foo']

The key must be a string and cannot be zero-length.  The value must also be a
string but is permitted to be zero-length.

Please consult the inline source documentation for the specifics of each
command available.

## Warnings

Data is not discarded from the cache until it is explicitly deleted with the
`cache.delete()` method.  Data does not persist after Supervisor is shut down.

Your Supervisor instance should never be exposed to the outside world.  It is
quite easy to perform a denial of service attack by filling `supervisor_cache`
with large amounts of data.

## Author

[Mike Naberezny](http://github.com/mnaberez)

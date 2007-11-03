supervisor_cache:
  This package is an RPC extension for the Supervisor package 
  that provides the ability to cache abritrary data in a 
  Supervisor instance as key/value pairs.
      
History
 
  Not yet released.

Overview

  Supervisor provides the "identification" configuration parameter that can be 
  returned by a Supervisor instance using supervisor.getIndentification().  
  This value cannot be modified at runtime.  
  
  Occasionally, it is useful to be able to store similar kinds of marker
  information in Supervisor and be able to modify it without restarting
  Supervisor. This is the use case for supervisor_cache. This package is not a
  replacement for systems like memcached.

Installation

  Install the package with the usual `python setup.py install` and then
  modify your supervisord.conf file to register the cache interface:
  
  [rpcinterface:cache]
  supervisor.rpcinterface_factory = supervisor_cache.rpcinterface:make_cache_rpcinterface  

  After modifying the supervisord.conf file, your supervisor instance must be
  restarted for the cache interface to be loaded.  
  
Usage

  The cache functions allow key/value pairs to be stored and fetched.  This
  Python interpreter session demonstrates the usage:

  >>> import xmlrpclib      
  >>> s = xmlrpclib.Server('http://localhost:9001')
  >>> s.cache.getKeys()
  []
  >>> s.cache.store('foo', 'bar')
  True
  >>> s.cache.fetch('foo')
  'bar'
  >>> s.cache.getKeys()
  ['foo']

  The key must be a string and cannot be zero-length.  The value must also be a
  string but is permitted to be zend-length.  Please consult the inline source 
  documentation for the specifics of each command available.

Warning
  
  Data is not discarded from the cache until it is explicitly deleted with the
  cache.delete() method.  Data does not persist after Supervisor is shut down.
  
  Your Supervisor instance should never be exposed to the outside world. It is
  quite easy to perform a denial of service attack by filling supervisor_cache
  it with large amounts of data.

Author Information

  Mike Naberezny (mike@maintainable.com)
  "Maintainable Software":http://www.maintainable.com

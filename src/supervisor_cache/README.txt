supervisor_cache:
  This package is an RPC extension for the supervisor2 package that
  provides the ability to cache limited amounts of data in the
  supervisor instance in key/value pairs.

History
 
  Not yet released.

Installation

  After installing the package with the usual `python setup.py install`, you
  need to modify your supervisord.conf file to register the cache interface:
  
  [rpcinterface:cache]
  supervisor.rpcinterface_factory = supervisor_cache.rpcinterface:make_cache_rpcinterface  

Author Information

  Mike Naberezny (mike@maintainable.com)
  "Maintainable Software":http://www.maintainable.com

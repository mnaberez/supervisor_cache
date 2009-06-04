__version__ = '0.2'

import urllib
import urllib2
if not hasattr(urllib2, 'splituser'):
    # setuptools wants to import this from urllib2 but it's not
    # in there in Python 2.3.3, so we just alias it.
    urllib2.splituser = urllib.splituser

from ez_setup import use_setuptools
use_setuptools()

import os
import sys
import string

version, extra = string.split(sys.version, ' ', 1)
maj, minor = string.split(version, '.', 1)

if not maj[0] >= '2' and minor[0] >= '3':
    msg = ("supervisor_cache requires Python 2.3 or better, you are "
           "attempting to install it using version %s.  Please install "
           "with a supported version" % version)

from setuptools import setup, find_packages
here = os.path.abspath(os.path.normpath(os.path.dirname(__file__)))

DESC = """\
supervisor_cache is an RPC extension for the supervisor package that
provides the ability to cache limited amounts of data in the
supervisor instance as key/value pairs."""

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: No Input/Output (Daemon)',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Topic :: System :: Boot',
    'Topic :: System :: Systems Administration',
    ]

dist = setup(
    name = 'supervisor_cache',
    version = __version__,
    license = 'License :: OSI Approved :: BSD License',
    url = 'http://maintainable.com/software/supervisor_cache',
    description = "supervisor_cache RPC extension for supervisor",
    long_description= DESC,
    classifiers = CLASSIFIERS,
    author = "Mike Naberezny",
    author_email = "mike@maintainable.com",
    maintainer = "Mike Naberezny",
    maintainer_email = "mike@maintainable.com",
    package_dir = {'':'src'},
    packages = find_packages(os.path.join(here, 'src')),
    # put data files in egg 'doc' dir
    data_files=[ ('doc', [
        'CHANGES.txt',
        'LICENSE.txt',
        'README.markdown',
        ]
    )],    
    install_requires = ['supervisor >= 3.0a6'],
    include_package_data = True,
    zip_safe = False,
    namespace_packages = ['supervisor_cache'],
    test_suite = 'supervisor_cache.tests'
    )

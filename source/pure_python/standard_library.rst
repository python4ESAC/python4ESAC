Standard Library
================

.. note:: Reference document for this section:

 * The Python Standard Library documentation: 
   http://docs.python.org/library/index.html

 * Python Essential Reference, David Beazley, Addison-Wesley Professional

``os`` module: operating system functionality
-----------------------------------------------

*"A portable way of using operating system dependent functionality."*

Directory and file manipulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Current directory::

    >>> os.getcwd()
    >>> '/Users/cburns/src/scipy2009/scipy_2009_tutorial/source'

List a directory::

    >>> os.listdir(os.curdir)
    ['.index.rst.swo',
     '.python_language.rst.swp',
     '.view_array.py.swp',
     '_static',
     '_templates',
     'basic_types.rst',
     'conf.py',
     'control_flow.rst',
     'debugging.rst',
     ...

Make a directory::

    >>> os.mkdir('junkdir')
    >>> 'junkdir' in os.listdir(os.curdir)
    True

Rename the directory:

    >>> os.rename('junkdir', 'foodir')

    >>> 'junkdir' in os.listdir(os.curdir)
    False

    >>> 'foodir' in os.listdir(os.curdir)
    True

    >>> os.rmdir('foodir')

    >>> 'foodir' in os.listdir(os.curdir)
    False

Delete a file:

    >>> fp = open('junk.txt', 'w')    # first create an empty file
    >>> fp.close()

    >>> 'junk.txt' in os.listdir(os.curdir)
    True

    >>> os.remove('junk.txt')

    >>> 'junk.txt' in os.listdir(os.curdir)
    False

``os.path``: path manipulations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``os.path`` provides common operations on pathnames::

    >>> fp = open('junk.txt', 'w')

    >>> fp.close()

    >>> a = os.path.abspath('junk.txt')

    >>> a
        '/Users/cburns/src/scipy2009/scipy_2009_tutorial/source/junk.txt'

    >>> os.path.split(a)
        ('/Users/cburns/src/scipy2009/scipy_2009_tutorial/source', 
       	 'junk.txt')

    >>> os.path.dirname(a)
        '/Users/cburns/src/scipy2009/scipy_2009_tutorial/source'

    >>> os.path.basename(a)
        'junk.txt'

    >>> os.path.splitext(os.path.basename(a))
        ('junk', '.txt')

    >>> os.path.exists('junk.txt')
        True

    >>> os.path.isfile('junk.txt')
        True

    >>> os.path.isdir('junk.txt')
        False

    >>> os.path.expanduser('~/local')
        '/Users/cburns/local'

    >>> os.path.join(os.path.expanduser('~'), 'local', 'bin')
        '/Users/cburns/local/bin'

Running an external command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  >>> from subprocess import call
  >>> call('chmod +x filename', shell=True)


``shutil``: high-level file operations
---------------------------------------

The ``shutil`` provides useful file operations:

    * ``shutil.rmtree``: Recursively delete a directory tree.
    * ``shutil.move``: Recursively move a file or directory to another location.
    * ``shutil.copy``: Copy files or directories.

``glob``: Pattern matching on files
-------------------------------------

The ``glob`` module provides convenient file pattern matching.

Find all files ending in ``.txt``::

    >>> from glob import glob

    >>> glob('*.txt')
    ['holy_grail.txt', 'junk.txt', 'newfile.txt']

    >>> glob('[hn]*.txt')
    ['holy_grail.txt', 'newfile.txt']

Note that by default the results aren't sorted. If you want the output
list sorted, use::

     >>> sorted(glob('[hn]*.txt'))


Environment variables:
~~~~~~~~~~~~~~~~~~~~~~
::

    >>> import os

    >>> os.environ.keys()
    ['_',
     'FSLDIR',
     'TERM_PROGRAM_VERSION',
     'FSLREMOTECALL',
     'USER',
     'HOME',
     'PATH',
     'PS1',
     'SHELL',
     'EDITOR',
     'WORKON_HOME',
     'PYTHONPATH',
     ...

    >>> os.environ['PYTHONPATH']
    '.:/Users/cburns/src/utils:/Users/cburns/src/nitools:
    /Users/cburns/local/lib/python2.5/site-packages/:
    /usr/local/lib/python2.5/site-packages/:
    /Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5'

    >>> os.getenv('PYTHONPATH')
    '.:/Users/cburns/src/utils:/Users/cburns/src/nitools:
    /Users/cburns/local/lib/python2.5/site-packages/:
    /usr/local/lib/python2.5/site-packages/:
    /Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5'




``sys`` module: system-specific information
--------------------------------------------

System-specific information related to the Python interpreter.

* Which version of python are you running and where is it installed::

    >>> sys.platform
    'darwin'

    >>> sys.version
    '2.5.2 (r252:60911, Feb 22 2008, 07:57:53) \n
    [GCC 4.0.1 (Apple Computer, Inc. build 5363)]'

    >>> sys.prefix
    '/Library/Frameworks/Python.framework/Versions/2.5'

* List of command line arguments passed to a Python script::

   >>> sys.argv
   ['/Users/cburns/local/bin/ipython']


``sys.path`` is a list of strings that specifies the search path for
modules.  Initialized from PYTHONPATH::

    >>> sys.path 
    ['',
     '/Users/cburns/local/bin',
     '/Users/cburns/local/lib/python2.5/site-packages/grin-1.1-py2.5.egg',
     '/Users/cburns/local/lib/python2.5/site-packages/argparse-0.8.0-py2.5.egg',
     '/Users/cburns/local/lib/python2.5/site-packages/urwid-0.9.7.1-py2.5.egg',
     '/Users/cburns/local/lib/python2.5/site-packages/yolk-0.4.1-py2.5.egg',
     '/Users/cburns/local/lib/python2.5/site-packages/virtualenv-1.2-py2.5.egg',
     ...


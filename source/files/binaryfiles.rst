:tocdepth: 2

Binary formats useful for astronomers
*************************************

Pyfits - Reading and writing fits files
=======================================

`PyFITS <http://packages.python.org/pyfits/>`_ is a Python module
developed at STScI to read and write all types of fits files. The full
html manual is available `here
<http://stsdas.stsci.edu/download/docs/pyfits/header-refactoring/#>`_.
The pdf version of the `manual
<http://stsdas.stsci.edu/download/docs/The_PyFITS_Handbook.pdf>`_ is
more than hundred pages long.

.. admonition:: External resource!

    The PyFITS tutorial itself is good for our purpose and since this
    is the internet I will not reinvent the wheel. Read the `Pyfits
    tutorial
    <http://packages.python.org/pyfits/users_guide/users_tutorial.html>`_
    then come back to this page for an exercise.

.. admonition::  Exercise

    Use the following code to download a fits file for this exercise::
        
        import urllib2, tarfile
        url = 'http://python4astronomers.github.com/core/core_examples.tar'
        tarfile.open(fileobj=urllib2.urlopen(url), mode='r|').extractall()
        cd py4ast/core
        ls

    Read in the fits file. Find the time and date of the
    observation, and read the intensity array.


.. raw:: html

   <p class="flip1">Click to Show/Hide Solution</p> <div class="panel1">

Here is a possible solution::
    
    import pyfits
    hdus = pyfits.open('3c120_stis.fits.gz')
    hdus.info()
    head = hdus[0].header
    head.keys()             # lists all keywords in a dictionary
    head['TDATEOBS']
    head['TTIMEOBS']
    img = hdus[1].data      # Intensity data

We can use ``plt.imshow()`` (matplotlib again) to display the
intensity array using some sensible minimum and maximum value so that
the spectrum is visible::

    plt.clf()
    plt.imshow(img, origin = 'lower', vmin = -10, vmax = 65)
    plt.colorbar()

We will revisit this piece of code in the :doc:`../core/numpy_scipy`
part of the tutorial.

.. raw:: html

   </div>

``pickle``: easy binary persistence
===================================

The Pickle package is in the Python standard library, is useful to
store arbitrary objects to a file.

  >>> import cPickle as pickle
  >>> l = [1, None, 'Stan']
  >>> pickle.dump(l, file('test.pkl', 'w'), protocol=2)
  >>> pickle.load(file('test.pkl'))
  [1, None, 'Stan']

The ``protocol`` keyword specifies the algorithm used to convert the
object into a binary file. ``protocol=2`` is fastest and creates the
smallest files, and should be preferred.

A drawback of the pickle format is that earlier versions of Python
than the version used to create the pickle may not be able to read
it. The higher the protocol level (level 2 is the highest), the less
likely an earlier version of Python can read the file. For this
reason it's best to restrict pickling to saving temporary
results. For long-term storage other binary formats, such as FITS or
HDF5, are better.

``json``: text file persistence
===============================

The ``json`` package in the standard library is similar to the
``pickle`` package, but it allows you to store Python objects as text
files in the json format, a sub-set of the XML format. In general this
is inefficient, as text files are slow to create and read compared to
binary files, and often result in larger file sizes. In addition, only
basin Python types can be saved (not Numpy arrays, for
example). However, they have the advantage of being easy to read in a
text editor, and the json format can be easily parsed by many other
programming languages (Java and C for example).

The process for creating and loading json files is similar to
pickling::

    import json
    d = {'name':'G0001', 'RA': 2.34531, 'Dec': -40.0112}
    json.dump(d, file('coord.jsn', 'w'))
    d = json.load(d, file('coord.jsn', 'r'))
    
    >>> d
    {u'Dec': -40.0112, u'RA': 2.34531, u'name': u'G0001'}

.. note:: 

  **Unicode:** The ``u`` in front of the strings in the dictionary
  after the json file has been read stands for unicode. This is
  because the strings are saved as unicode. Mostly you can ignore the
  difference between ascii and unicode strings for scientific
  programming, but for more information see `here
  <http://docs.python.org/howto/unicode.html>`_. Unifying the ascii
  and unicode types into a single string type is one of the major
  changes between Python 2.x and Python 3.

Reading IDL .sav files
======================

IDL is still a very common tool in astronomy. While IDL packages exist
to read and write data in simple (ASCII) or standardized file formats
(fits), that users of all platforms can use, IDL also offers a binary
file format with an undocumented, proprietary structure. However,
acess to this file format (usually called ``.sav``) is very simple and
convenient in IDL. Therefore, many IDL users dump their data in this
way and you might be forced to read ``.sav`` files a colleague has
sent you.

Here is an examplary ``.sav`` :download:`file
<../downloads/myidlfile.sav>`.  If you have trouble downloading the
file, then use IPython::

    import urllib2
    url = 'http://python4astronomers.github.com/_downloads/myidlfile.sav'
    open('myidlfile.sav', 'wb').write(urllib2.urlopen(url).read())
    ls

What can you do?
    1. Convert your colleague to use a different file format.
    2. Read that file in python.

If you have a relatively recent version (at least 0.9) of ``scipy``
then this is a matter of two lines::
    
    from scipy.io.idl import readsav
    data = readsav('myidlfile.sav')

If your scipy is older, then you need to install the package `idlsave
<http://astrofrog.github.com/idlsave/>`_ yourself.  (Go back to
:doc:`../installation/packages` for details on package installation.)

In a normal terminal (outside ``ipython``) do::
    
    pip install --upgrade idlsave
    
or, if you install packages as root user on your system::
    
    sudo pip install --upgrade idlsave

Then import the package and read the data::
    
    import idlsave
    data = idlsave.read('myidlfile.sav')
    
.. admonition::  Exercise: Where is your data?

    ``idlsave`` already prints some information on the screen while
    reading the file. Inspect the object ``data``, find out how you
    use it to access the ``x`` and ``y`` data in it.  Note you may get
    an error saying ``KeyError: 'rewrite'``. This can be ignored (it's
    a bug involving IPython and SciPy).  You can still use tab
    completion to look at the attributes and methods of ``data``.

.. raw:: html

   <p class="flip2">Click to Show/Hide Solution</p> <div class="panel2">

``data`` is a dictionary and all the variables in the ``.sav`` file
are fields in this dictionary. You get a list with
``data.keys()``. Then, this is easy::
    
    data['x']
    data['y']

.. raw:: html

   </div>

Note that ``idlsave`` cannot write files and that it will fail to read
if the ``.sav`` file contains special structures like system variables
or compiled IDL code.

.. include:: ../references.rst


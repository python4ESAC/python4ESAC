:tocdepth: 2

NumPy
-----

`NumPy`_ is at the core of nearly every scientific Python application or
module since it provides a fast N-d array datatype that can be manipulated in a
vectorized form.  This will be familiar to users of IDL or Matlab.

NumPy has a good and systematic `basic tutorial
<http://www.scipy.org/Tentative_NumPy_Tutorial>`_ available.  It is highly
recommended that you read this tutorial to fill in the gaps left by this
workshop, but on its own it's a bit dry for the impatient astronomer.

Here we'll learn NumPy by performing a very simple reduction of a
2-dimensional long slit spectrum (3C120 from HST/STIS):

- Read in the 2-d image
- Plot the spatial profile and raw spectrum
- Filter cosmic rays from the background
- Fit for the background and subtract
- Sum the source signal

+------------------------------------+-----------------------------------+
|  **2-d longslit image**            |   **Final 1-d spectrum**          |
+====================================+===================================+
| .. image:: 3c120.png               | .. image:: 3c120_spec.gif         |
|    :scale: 70                      |    :scale: 45                     |
+------------------------------------+-----------------------------------+


.. Topics:
   - Appending
   - Median
   - Making arrays
   - Broadcasting x = arange(5); y=x.reshape(5,1) ; x + y * 10
   - diff between list and array
   - vectorized ops (do a for loop)
   - exercise: make a mexican hat or similar
   - boolean masking / where
   - scipy 2-d median filter


.. raw:: html

   <p class="flip0">Why NumPy? (Click to Show/Hide)</p> <div class="panel0">

.. admonition:: INFO

    Python's ease-of-use often comes at a price: speed. Let's try to compute the
    sine of 20 million (uniform) random floats using Python's standard modules, and
    time it.
        

    ::

        import time # get access to CPU time
        import math # standard module implementing mathematical operators
        import random # generate random numbers
            
        t0 = time.time()    
        output = []
        for i in range(20000000):
            output.append(math.sin(random.random()))
        print time.time()-t0

    This needs **13.3424** seconds (on a Dell Dual Core Genuine Intel(R), T2600, 2.16GHz, 32-bit processor) of execution time. We can gain ~50% with some
    tricks (list comprehension, generator and local variables):

    ::

        sin,rand = math.sin,random.random
        output = [sin(rand()) for i in xrange(20000000)] # in Python 3, replace xrange with range

    Which tops at **8.6610** seconds. With numpy, we can gain another 50%, **and**
    have a much cleaner implementation:

    ::

        output = np.sin(np.random.uniform(size=20000000))

    The latter takes **3.9020** seconds to run. A pure FORTRAN program is, however,
    still almost 50% faster than numpy (2.2641 seconds).

    Basically, numpy provides vectorized functions written in C or FORTRAN that
    can act on pure Python objects, with a little bit of function-call overhead.
    Most of the looping is done in C or FORTRAN, avoiding the expensive ``for``
    loops in pure Python.

    Sometimes doing things in a vectorized way is not possible or just too
    confusing.  There is an art here and the basic answer is that if it runs
    fast enough then you are good to go.  Otherwise things need to be vectorized
    or maybe coded in C or Fortran.

.. raw:: html

   </div>



Setup
^^^^^^^^

Before going further you need to get the example data and script files for
the workshop.  Now that you have a working Python installation we can do this
without worrying about details of the platform (e.g. linux has wget,
Mac has curl, Windows might not have tar, etc etc).

Now start IPython (``ipython --pylab``) or use your existing session and enter:

.. ipython::

  In [1]: import urllib2, tarfile
  
  In [1]: url = 'http://python4astronomers.github.com/core/core_examples.tar'
  
  In [1]: tarfile.open(fileobj=urllib2.urlopen(url), mode='r|').extractall()
  
  In [1]: cd py4ast/core
  
  In [1]: ls


Leave this IPython session open for the rest of the workshop.

.. admonition:: Exercise (for the interested reader): How did that code above work?

   Explain what's happening in each part of the previous code snippet to grab
   the file at a URL and untar it.  Google on "python urllib2" and "python
   tarfile" to find the relevant module docs.  Figure out how you would
   use the ``tarfile`` module to create a tarfile.

.. raw:: html

   <p class="flip1">Click to Show/Hide Solution</p> <div class="panel1">

- ``urllib2.urlopen(url)`` opens the URL as a streaming file-like object
- ``mode='r|' means ``tarfile`` is expecting a streaming file-like object
  with no ability to seek in the file
- ``tarfile.open(..).extractall`` then extracts the tar archive

Creating a tarfile is left for the reader to solve.

.. raw:: html

   </div>

Read in the 2-d image
^^^^^^^^^^^^^^^^^^^^^^

First read in the long-slit spectrum data.  The standard file format available
for download from `MAST <http://archive.stsci.edu/hst/>`_ is a FITS file with
three identically sized images providing the 2-d spectral intensity, error
values, and data quality for each pixel.  The slit direction is along the rows
(up and down) and wavelength is in columns (left to right).

.. ipython::

  In [1]: import pyfits
  
  In [1]: hdus = pyfits.open('3c120_stis.fits.gz')
  
  In [1]: hdus

Type ``?hdus`` to get a little more detail on the ``hdus`` object.

Now give meaningful names to each of the three images that are available in the
FITS HDU list.  You can access element ``n`` in a list with the index ``[n]``,
where the count starts from 0:

.. ipython::

  In [1]: primary = hdus[0].data  # Primary (NULL) header data unit
  
  In [1]: img = hdus[1].data      # Intensity data
  
  In [1]: err = hdus[2].data      # Error per pixel
  
  In [1]: dq = hdus[3].data       # Data quality per pixel

.. raw:: html

   <p class="flip2">Click to Show/Hide Tip: pyFITS </p> <div class="panel2">

.. admonition:: TIP: pyFITS

    The HDUList from a FITS file acts like an ordered dictionary: instead of accessing
    via an index ``n``, you can also access the extensions by *name*:

    .. ipython::

      In [1]: img = hdus['SCI'].data      # Intensity data
      
      In [1]: err = hdus['ERR'].data      # Error per pixel
      
      In [1]: dq = hdus['DQ'].data       # Data quality per pixel

    You can find (and set) the name of an extension throught the header keyword
    ``EXTNAME`` (case-insensitive).

    .. ipython::
    
      In [1]: hdus[1].header['extname']

    A frequently used convention is to store scientific data in an extension named
    ``SCI``. For more information on FITS files and pyFITS, see the `pyFITS documentation <http://stsdas.stsci.edu/download/wikidocs/The_PyFITS_Handbook.pdf>`_
    
.. raw:: html

   </div>


Next have a look at the images using one of the standard Matplotlib plotting
functions:

.. ipython::

  In [1]: import pylab as plt # not needed when you run ipython with the pylab option

  In [1]: import numpy as np  # not needed when you run ipython with the pylab option

  In [1]: plt.imshow(img)

.. raw:: html

   <p class="flip4">Click to Show/Hide Tip: matplotlib widget</p> <div class="panel4">

.. admonition:: TIP: matplotlib widget

    The matplotlib widget that appears when you make a plot in IPython (or whenever
    you call ``plt.show()`` in a script), is highly interactive. You can:
    
    * *zoom in* by clicking on the *zoom* icon and dragging a rectangle
    * *pan* by clicking on the *pan* icon and dragging the image around
    * *pan* and *zoom* by clicking on the *pan* icon, click, hold and drag with the right mouse button.
    
.. raw:: html

   </div>

As you can see, it is hard to see things. So, let's set a few option for this
plot. First, we want the origin in the lower left instead of the upper left
corner:

.. ipython::
    
    In [1]: plt.clf()

    In [1]: plt.imshow(img, origin = 'lower')

Second, let's change the scaling to something more sensible. By default,
``plt.imshow()`` scales the colorbar from the minimum to the maximum value. In
our case that is not the best option. We can set a lower and upper bound and
add a colorbar to our plot:

.. ipython::

    In [1]: plt.clf()

    In [1]: plt.imshow(img, origin = 'lower', vmin = -10, vmax = 65)

    In [1]: plt.colorbar()

Your plot should not look like this (it is possible that the colormap differs,
if your matplotlib has different defaults set).

.. image:: imgview_img.png
  :scale: 50

.. admonition:: Exercise: View the error and data quality images

  Bring up a viewer window for the other two images.  Play with the toolbar
  buttons on the lower-left (hint: try the four on the right first, then
  imagine a web browser for the three on the left).  Does the save button
  work for you?

.. raw:: html

   <p class="flip5">Click to Show/Hide Solution</p> <div class="panel5">

::
  
  # Errors
  plt.clf()
  plt.imshow(err, origin = 'lower', vmin = 5, vmax = 25)
  plt.colorbar()
  # Data quality
  plt.clf()
  plt.imshow(dq, origin = 'lower', vmax = 25)
  plt.colorbar()

.. image:: imgview_err.png
   :scale: 50

.. image:: imgview_dq.png
   :scale: 50

.. raw:: html

   </div>

Now discover a little bit about the images you have read in, first with ``?``::

  img?

Next use ``help`` and note the slightly different information that you get::

  help(img)

Use tab completion to see all the methods in short form::

  img.<TAB>

Finally find the shape of the image and its minimum value:

.. ipython::

  In [1]: img.shape  # Get the shape of img

  In [1]: img.min()  # Call object method min with no arguments


NumPy basics
^^^^^^^^^^^^

Before going further on the spectral extraction project we need to learn about
a few key features of NumPy.

Making arrays
#############

Arrays can be created in different ways:

.. ipython::

  In [1]: a = np.array([10, 20, 30, 40])   # create an array from a list of values

  In [1]: a

  In [1]: b = np.arange(4)                 # create an array of 4 integers, from 0 to 3
  
  In [1]: b

  In [1]: np.linspace(-np.pi, np.pi, 5)      # create an array of 5 evenly spaced samples from -pi to pi
  
  In [1]: np.logspace(1,3,9) # create a log-spaced array of 9 floats between (and including) 10 and 1000

The function ``arange`` is better only used when working with integer arguments.

.. raw:: html

   <p class="flip6">Click to Show/Hide Tip: creating sequences of numbers </p> <div class="panel6">

.. admonition:: TIP: creating sequences of numbers

    A general interface for creating arrays in provided by ``np.mgrid``. The syntax
    is slightly different than before, because it uses index slices instead of arguments.

    .. ipython::

      In [1]: np.mgrid[0:5:1]
  
      In [1]: np.mgrid[0:5:10j]

    And in more dimensions:

    .. ipython::

      In [1]: x,y = np.mgrid[-1:3:5j,0:2:0.5]

      In [1]: x
  
      In [2]: y

    
.. raw:: html

   </div>
  
New arrays can be obtained by operating with existing arrays:

.. ipython::

  In [1]: a + b**2            # elementwise operations


Arrays may have more than one dimension:

.. ipython::

  In [1]: f = np.ones([3, 4])                 # 3 x 4 float array of ones
  
  In [1]: f

  In [1]: g = np.zeros([2, 3, 4], dtype=int)  # 3 x 4 x 5 int array of zeros
  
  In [1]: g

  In [1]: i = np.zeros_like(f)                # array of zeros with same shape/type as f


You can change the dimensions of existing arrays:

.. ipython::

  In [1]: w = np.arange(12)

  In [1]: w.shape = [3, 4]       # does not modify the total number of elements

  In [1]: w

  In [1]: x = np.arange(5)
  
  In [1]: x
 
  In [1]: y = x.reshape(5, 1)
  
  In [1]: y = x.reshape(-1, 1)  # Same thing but NumPy figures out correct length
  
  In [1]: y
  
It is possible to operate with arrays of different dimensions as long as they fit well (broadcasting):

.. ipython::

  In [1]: x + y * 10

.. warning::
    
    Lists and array behave fundamentally different!

    .. ipython::
    
      In [1]: mylist = [1,2,3]
      
      In [2]: myarray = np.array([1,2,3])
      
      In [3]: mylist*2
      
      In [3]: myarray*2
  
.. admonition:: Exercise: Make a ripple

  Calculate a surface ``z = cos(r) / (r + 5)`` where ``r = sqrt(x**2 +
  y**2)``.  Set ``x`` to an array that goes from -20 to 20 stepping by 0.25
  Make ``y`` the same as ``x`` but "transposed" using the ``reshape`` trick above.
  Use `plt.imshow` to display the image of ``z``.

.. raw:: html

   <p class="flip7">Click to Show/Hide Solution</p> <div class="panel7">

.. ipython::

   In [1]: x = np.arange(-20, 20, 0.25)

   In [1]: y = x.reshape(-1, 1)

   In [1]: r = np.sqrt(x**2 + y**2) # note the broadcasting behaviour

   In [1]: z = np.cos(r) / (r + 5)

   In [1]: plt.imshow(z, origin = 'lower)

or alternatively:

.. ipython::

   In [1]: x,y = np.mgrid[-20:20:200j,-20:20:200j]

   In [1]: r = np.sqrt(x**2 + y**2) # broadcasting not needed because x and y have the same shape
   
   In [1]: z = np.cos(r) / (r + 5)

   In [1]: plt.imshow(z, origin = 'lower)

.. image:: ripple.png
   :scale: 50

.. raw:: html

   </div>


Array access and slicing
############################

NumPy provides powerful methods for accessing array elements or particular subsets of an array,
e.g. the 4th column or every other row.  This is called slicing.  The outputs
below illustrate basic slicing, but you don't need to type these examples:

.. ipython::

   In [1]: a = np.arange(20).reshape(4,5)
   
   In [1]: a
   
   In [1]: a[2, 3]   # select element in row 2, col 3 (counting from 0)

   In [1]: a[2, :]   # select every element in row 2
   
   In [1]: a[:, 0]   # select every element in col 0

   In [1]: a[0:3, 1:3]

As a first practical
example plot column 300 of the longslit image to look at the spatial profile:

.. ipython::

  In [1]: plt.figure()             # make a new figure -- by default matplotlib overplots.
  
  In [1]: plt.plot(img[:, 300])

Note that as long as you don't close existing figures, they will be kept in memory.
If you want to close the current figure, call ``plt.close()``. If you want to
close all figures call ``plt.close('all')``.

.. image:: img_col300.png
  :scale: 50

The full slicing syntax also allows for a step size::

  <slice> = i0:i1:step
  array[<slice0>, <slice1>, ...]

- ``i0`` is the first index value (default is zero if not provided)
- ``i1`` is the index upper bound (default is last element index + 1)
- ``step`` is the step size (default is one).  When ``step`` is not specified then the final ":" is not required.

.. admonition:: Exercise: Slice the error array

  - For row 254 of the error array ``err`` plot columns 10 to 200 stepping by 3.
  - Print a rectangular region slice of the data quality with rows 251 to 253 (inclusive) and columns 101 to
    104 (inclusive).  What did you learn about the index upper bound value?

.. raw:: html

   <p class="flip8">Click to Show/Hide Solution</p> <div class="panel8">

.. ipython::

  In [1]: plt.clf()

  In [2]: plt.plot(err[254, 10:200:3])

  In [3]: dq[251:254, 101:105]

The index upper bound ``i1`` is one more than the final index that gets
included in the slice.  In other words the slice includes everything up to,
*but not including*, the index upper bound ``i1``.  There are good reasons for
this, but for now just accept and learn it.

.. image:: err_row254.png
   :scale: 50

.. raw:: html

   </div>

Plot the spatial profile and raw spectrum
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Plot the spatial profile by summing along the wavelength direction:

.. ipython::

  In [1]: profile = img.sum(axis=1)
  
  In [2]: plt.figure()

  In [3]: plt.plot(profile)

Now plot the spectrum by summing along the spatial direction:

.. ipython::

  In [1]: spectrum = img.sum(axis=0)
  
  In [1]: plt.figure()
  
  In [1]: plt.plot(spectrum)

Since most of the sum is in the background region there is a lot of noise and
cosmic-ray contamination.

.. image:: profile.png
   :scale: 50

.. image:: spectrum_noisy.png
   :scale: 50

.. admonition:: Exercise: Use slicing to make a better spectrum plot

  Use slicing to do the spectrum sum using only the rows in the image where
  there is a signal from the source.
  Hint: zoom into the profile plot to find the right row range.

.. raw:: html

   <p class="flip9">Click to Show/Hide Solution</p> <div class="panel9">

.. ipython::

  In [1]: spectrum = img[250:260, :].sum(axis=0)

  In [1]: plt.clf()

  In [1]: plt.plot(spectrum)

.. image:: spectrum_clean.png
   :scale: 50

.. raw:: html

   </div>

.. Solution


Filter cosmic rays from the background
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Plot five columns (wavelength) from the spectrum image as follows:

.. ipython::

  In [1]: plt.clf()

  In [1]: plt.plot(img[:, 254:259])

.. image:: img_row254_noisy.png
   :scale: 50

The basic idea in spectral extraction is to subtract out the background and sum
over rows with the source signal.

It's evident that there are significant cosmic ray defects in the data.  In
order to do a good job of subtracting the background we need to filter them
out.  Doing this correctly in general is difficult and in reality one would
just use the answers already provided by STSci.

**Strategy**: Use a median filter to smooth out single-pixel deviations.  Then
use sigma-clipping to remove large variations between the actual and smoothed
image.

.. ipython::

  In [1]: import scipy.signal

  In [1]: img_sm = scipy.signal.medfilt(img, 5)

  In [1]: sigma = np.median(err)

  In [1]: bad = np.abs(img - img_sm) / sigma > 8.0

  In [1]: img_cr = img.copy()

  In [1]: img_cr[bad] = img_sm[bad]

  In [1]: img_cr[230:280,:] = img[230:280,:]  # Filter only for background

Check if it worked:

.. ipython::

  In [1]: plt.clf()

  In [1]: plt.plot(img_cr[:, 254:259])

.. image:: img_row254_clean.png
   :scale: 50

This introduces the important concept of slicing with a **boolean mask**.  Let's
look at a smaller example:

.. ipython::

   In [1]: a = np.array([1, 4, -2, 4, -5])
   
   In [1]: neg = (a < 0)    # Parentheses here for clarity but are not required

   In [1]: neg

   In [1]: a[neg] = 0
   
   In [1]: a

A slightly more complex example shows that this works the same on N-d arrays
and that you can compose logical expressions:

.. ipython::

   In [1]: a = np.arange(25).reshape(5,5)

   In [1]: ok = (a > 6) & (a < 17)     # "ok = a > 6 & a < 17" will FAIL!

   In [1]: a[~ok] = 0                  # Note the "logical not" operator

   In [1]: a
   
.. admonition:: Exercise [intermediate]: circular region slicing

   Remember the surface ``z = cos(r) / (r + 5)`` that you made previously.  Set
   ``z = 0`` for every pixel of ``z`` that is within 10 units of (x,y) = (10, 15).

.. raw:: html

   <p class="flip10">Click to Show/Hide Solution</p> <div class="panel10">

.. ipython::

  In [1]: dist = np.sqrt((x-10)**2 + (y-15)**2)
  
  In [1]: mask = dist < 10
  
  In [1]: z[mask] = 0
  
  In [1]: plt.imshow(z, origin = 'lower')

.. image:: ripple_masked.png
   :scale: 50

.. raw:: html

   </div>

.. admonition:: Detour: copy versus reference

   **Question**
     In the median filtering commands above we wrote ``img_cr = img.copy()``.  Why
     was that needed instead of just ``img_cr = img``?

   **Answer**
     Because the statement ``img_cr = img`` would just create another reference
     pointing to the underlying N-d array object that ``img`` references.

   Variable names in Python are just pointers to the actual Python
   object.  To see this clearly do the following:

.. ipython::

     In [1]: a = np.arange(8)
     
     In [1]: b = a
     
     In [1]: id(a)     # Unique identifier for the object referred to by "a": arange(8)
     
     In [1]: id(b)     # Unique identifier for the object referred to by "b": same ^^
     
     In [1]: b[3] = -10
     
     In [1]: a

   After getting over the initial confusion this behavior is actually a good
   thing because it is efficient and consistent within Python.  If you really
   need a copy of an array then use the copy() method as shown.

   **BEWARE** of one common pitfall: NumPy "basic" slicing like ``a[3:6]``
   does NOT make a copy:

.. ipython::

     In [1]: b = a[3:6]
     
     In [1]: b

     In [1]: b[1] = 100
     
     In [1]: a

   However if you do arithmetic or boolean mask then a copy is always made:

.. ipython::

     In [1]: a = np.arange(4)
     
     In [1]: b = a**2
     
     In [1]: a[1] = 100
     
     In [1]: a

     In [1]: b    # Still as expected after changing "a"

Fit the background
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To subtract the background signal from the source region we want to fit a
quadratic to the background pixels and subtract that quadratic from the entire
image which includes the source region.

Let's tackle a simpler problem first and fit the background for a single column:

.. ipython::
    
    In [1]: x = np.append(np.arange(10, 200), np.arange(300, 480))  # Background rows
    
    In [1]: y = img_cr[x, 10]         # Background rows of column 10 of cleaned image
    
    In [1]: plt.figure()
    
    In [1]: plt.plot(x, y)
  
    In [1]: pfit = np.polyfit(x, y, 2)   # Fit a 2nd order polynomial to (x, y) data
    
    In [1]: yfit = np.polyval(pfit, x)   # Evaluate the polynomial at x
   
    In [1]: plt.plot(x, yfit)
   
    In [1]: plt.grid()

.. image:: bkg_fit0.png
   :scale: 50

Now do this for every column and store the results in a background image:

.. ipython::

  In [1]: xrows = np.arange(img_cr.shape[0])          # Array from 0 .. N_rows-1

  In [1]: bkg = np.zeros_like(img_cr)                 # Empty image for background fits

  In [1]: for col in np.arange(img_cr.shape[1]):      # Iterate over columns
     ...:     pfit = np.polyfit(x, img_cr[x, col], 2) # Fit poly over bkg rows for col
     ...:     bkg[:, col] = np.polyval(pfit, xrows)   # Eval poly at ALL row positions
     ...:

  In [1]: plt.clf()

  In [1]: plt.imshow(bkg, origin = 'lower', vmin=0, vmax=20)

  In [1]: plt.colorbar()

.. image:: bkg_fit1.png
   :scale: 50

Finally subtract this background and see if it worked:

.. ipython::

  In [1]: img_bkg = img_cr - bkg
  
  In [1]: plt.clf()
  
  In [1]: plt.imshow(img_bkg, origin = 'lower', vmin=0, vmax=60)
  
  In [1]: plt.colorbar()


+------------------------------------+-----------------------------------+
|  **Background subtracted**         |   **Original**                    |
+====================================+===================================+
| .. image:: bkg_fit2.png            | .. image:: imgview_img.png        |
|    :scale: 50                      |    :scale: 50                     |
+------------------------------------+-----------------------------------+

.. Solution
   badimg = np.zeros(bad.shape)
   badimg[bad] = 1
   ImgView(badimg)

Sum the source signal
^^^^^^^^^^^^^^^^^^^^^^

Now the final step is easy and is left as an exercise.

+------------------------------------+-----------------------------------+
|**Python for Astronomers Spectrum** |   **HST official spectrum**       |
+====================================+===================================+
| .. image:: spectrum_final.png      | .. image:: 3c120_spec.gif         |
|    :scale: 50                      |    :scale: 45                     |
+------------------------------------+-----------------------------------+

.. admonition:: Exercise: Make the final spectrum

   Sum the rows of the background subtracted spectrum and plot.  Hint: you
   already did it once in a previous exercise.

.. raw:: html

   <p class="flip6">Click to Show/Hide Solution</p> <div class="panel6">

::

  spectrum = img_bkg[250:260, :].sum(axis=0)
  plt.clf()
  plt.plot(spectrum)

.. raw:: html

   </div>


**To do**: flux calibration and wavelength calibration!

SciPy
-----

It is impossible to do justice to the full contents of the `SciPy`_ package: is
entirely too large!  What is left as homework for the reader is to
click through to the main `SciPy Reference Manual
<http://docs.scipy.org/doc/scipy/reference/>`_ and skim the `tutorial
<http://docs.scipy.org/doc/scipy/reference/tutorial/index.html>`_.  Keep
this repository of functionality in mind whenever you need some numerical
functionality that isn't in NumPy: there is a good chance it is in SciPy:

- Basic functions in Numpy (and top-level scipy)
- Special functions (scipy.special)
- Integration (scipy.integrate)
- Optimization (optimize)
- Interpolation (scipy.interpolate)
- Fourier Transforms (scipy.fftpack)
- Signal Processing (signal)
- Linear Algebra
- Statistics
- Multi-dimensional image processing (ndimage)
- File IO (scipy.io)
- Weave


.. _guide:


ESAC Python Workshop
====================

About this website
------------------

This Python course for ESAC is adapted from the `Practical Python for
Astronomers <http://python4astronomers.github.com>`_ course written by Tom
Aldcroft, Tom Robitaille, Brian Refsdal, Gus Muench (Copyright 2011,
Smithsonian Astrophysical Observatory) and released under a `Creative Commons
Attribution 3.0 License <http://creativecommons.org/licenses/by/3.0>`_.

The present course has been restructured and adapted to reflect the interests
of the ESAC audience.


About the course
================

The ESAC Python course is a series of hands-on workshops to explore
the Python language and the powerful analysis tools it provides. *The
emphasis is on using Python to solve real-world problems that
astronomers are likely to encounter in research.*

- The workshops immediately make use of the full suite of plotting,
  analysis, and file reading tools.
- Along the way elements of the Python language such as data types,
  control structures, functions, and objects are introduced.
- This is an interactive experience using tutorial examples run by
  participants on their laptops.


**Workshop topics**

.. toctree::
   :maxdepth: 1

   installation/installation
   intro/intro
   pure_python/pure_python
   files/files
   core/core
   plotting/plotting
   fitting/fitting
   vo/vo

.. toctree::
   :hidden:

   local/local.rst

Sample Workshop Schedule
-------------------------

The workshop schedule is as follows.  Except for the first introductory session all
workshops are hands-on and participants should bring a laptop.

======== ======================================= ============== =========
Date     Topic                                   Time           Presenter
======== ======================================= ============== =========
30th May Installation and Understanding Packages 9:30-10:00     Eli
30th May Introduction to Python for ESAC         10:00-11:00    Eli
30th May Introduction to Pure Python             11:30-13:00    Neil
30th May Reading and Writing Files               14:00-15:30    Neil
30th May IPython, Numpy and Scipy                15:45-17:00    Pieter
31st May IPython, Numpy and Scipy continued      9:30-11:00     Pieter
31st May Introduction to Matplotlib              11:30-13:00    Pieter
31st May Publication quality plots               14:00-15:30    Neil
31st May Plotting images and APLpy               15:45-17:00    Eli
1st June APLpy continued                         9:30-11:00     Eli
1st June Fitting and modelling, Q&A              11:30-13:00    Eli
1st June urllib2, ATPy, examples                 14:00-15:30    Neil
1st June multiprocessing, f2py, more examples    15:45-17:00    Pieter
======== ======================================= ============== =========

About the Workshops
-------------------

The content presented here is suitable for self-study by those wishing to learn
Python for astronomy or other scientific research applications.

**A greater goal is for those knowledgable in Python to teach the workshop
series at their local institutions, adapting the content as desired.** To that
end we have developed the content in `Sphinx <http://sphinx.pocoo.org>`_
RestructuredText and hosted the source on github at
`<https://github.com/python4astronomers/>`_.  Anyone interested can clone the
repository or download a tarball and make modifications needed to present the
material locally.

We would also welcome comments, fixes, or suggestions for improvement.  This
can be done as a Github issue or pull request, or by sending email to
aldcroft@head.cfa.harvard.edu.

The workshop material here was presented in the Spring of 2011 at the Harvard /
Smithsonian Center for Astrophysics.  A range of about 25 to 50 people
participated in the different workshops, which were 1.5 hours in duration.
Based on our experience a 2 hour slot would have been more reasonable to allow
time for the exercises and discussion.

About the Format
-----------------

The workshop presentations are formatted as Sphinx web documents instead of the
more traditional slide presentation.  This was a natural choice for the
authors who all use `Sphinx`_ for Python documenation.  Further inspiration was
drawn from `Dumping PowerPoint in Favor of Web Sites
<http://www.sal.ksu.edu/faculty/tim/prof-day/index.html>`_.  This site
highlights by discussion and examples the advantages in using a web-based study
guide.  In particular we found the non-linear format (e.g. jumping to different
sections or web sites) and ability to show longer examples were quite valuable.

Having full prose text results in a document which is far more useful as a
standalone study guide than presentation slides.  Ironically it also reduces
the temptation to read from the screen.

+---+
|   |
+---+

.. :Authors: Tom Aldcroft, Tom Robitaille, Brian Refsdal, Gus Muench
.. :Copyright: 2011 Smithsonian Astrophysical Observatory

:tocdepth: 2

Miscellaneous formats
=====================

These pages show a way to read most of the files astronomers will need
in their day-to-day work.  However, no format is so obscure that it
could not be used and there are certainly files out there that will
not fall into one of the categories above.  Here are some hints:

* If it is an ASCII file, often some manual editing will do the job.
  E.g. in a space-separated table there are missing values::

    col1 col2 col3
    aaaa  1    2
    bbbb       3
    cccc  4    5

  In a text editor put ``nan`` in the empty space and ``asciitable``
  will read the file.

* Google. No file format is too obscure to find a reader for it.
* When writing files, use standard formats like FITS, ascii, HDF5 and
  not your personal, undocumented binary format.

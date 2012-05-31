IPython
=======

.. contents::


Running IPython for the first time
----------------------------------

IPython is an enhanced Python shell that creates a comprehensive environment for
interactive and exploratory computing. In this section we’ll learn the basic
features of IPython and how it benefits interactive analysis.

Before going further, open a new terminal window and change to your main working
directory. Then start IPython by typing ``ipython --pylab`` at the command prompt::

    $:> ipython

The first time you start the ipython shell, a hidden directory ``.ipython`` will
be created in your home directory (``/home/user/`` on unix or ``C:\\Documents and
Settings\user`` on Windows, henceforth called ``IPYTHONDIR``).

It can be useful to always execute a standard block of code when you start
IPython. For example, if you always want to have access to the standard ``glob``
and ``os`` modules, you can write a small script only containing::

    import glob
    import os

And save it to ``IPYTHONDIR/pythonstartup.py`` for example. Then, add the following line
to the ``IPYTHONDIR/ipythonrc`` file::

    execfile IPYTHONDIR/pythonstartup.py

Next time you start the IPython shell, the two modules will be loaded.

To exit IPython, hit <CTLR+D> or type ``exit`` or ``quit`` in the shell.

.. admonition:: TIP: a MATLAB style environment

    There is an easy way to automatically load the basic numerical and graphical
    packages. When starting IPython in a terminal, simply add ``-- pylab`` to
    the command::
    
        $:>ipython --pylab
    
    Extra benefit: when you normally load ``pylab`` and a plot is shown to the
    screen with ``pl.show()``, you have to close the plot if you want to continue
    working in the shell. With the ``--pylab`` option, plots are shown in a
    separate thread, allowing you to simultaneously edit data and view a plot:
        
    .. sourcecode:: ipython
    
        In [1]: x = np.arange(0,10,0.2)
        
        In [2]: y = np.sin(x)
        
        In [3]: print x
        [ 0.   0.2  0.4  0.6  0.8  1.   1.2  1.4  1.6  1.8  2.   2.2  2.4  2.6  2.8
          3.   3.2  3.4  3.6  3.8  4.   4.2  4.4  4.6  4.8  5.   5.2  5.4  5.6  5.8
          6.   6.2  6.4  6.6  6.8  7.   7.2  7.4  7.6  7.8  8.   8.2  8.4  8.6  8.8
          9.   9.2  9.4  9.6  9.8]
          
        In [4]: plot(x,y)

Keyboard navigation and history
-------------------------------

One of the most useful features of IPython is the ability to edit and navigate
your command line history. This lets you quickly re-do commands, perhaps with a
slight variation based on seeing the last result. Try cut-n-pasting the above
lines in an IPython session. This should bring up a plot of a sine wave.

Now hit up-arrow once and get back the ``plot(x, y)`` line. Hit the left-arrow
key (not backspace) once and type ``**2`` so that the line reads ``plot(x, y**2)``.
Now you can hit Return to see the new curve overlayed within the same plot window.
It is not necessary to forward-space to the end of the line, you can hit Return
with the cursor anywhere in the line.

Now say you want to change the x values slightly. One option is to just hit the
up-arrow 5 times, but a much faster way is to remember that the line started with
``x``, so type ``x`` and then start hitting up-arrow. Only lines that start with
``x`` will be displayed and you are immediately at the ``x = arange(0, 10, 0.2)``
line. Now use the right-arrow and backspace to change ``10`` to ``15`` and hit
Return. Of course ``y`` needs to be recalculated, so hit ``y`` then up-arrow, then
Return. Nice and fast!

Your command history is saved between sessions (assuming that you exit IPython
gracefully) so that when you start a new IPython you can use up-arrow to re-do
old commands. You can view your history within the current session by entering
history.

Linux and shell commands
------------------------

A select set of useful linux commands are available from the IPython prompt.
These include ``ls``, ``pwd``, ``cd``, and ``rm``. Any shell command can be
executed by preceding it with an exclamation point ``!``.

Tab completion
--------------

IPython has a very useful tab completion feature that can be used both to
complete file names and to inspect python objects. As an example do:

.. sourcecode:: ipython

    In [5]: ls ~/<TAB>

This will list everything in your home directory. You can continue this way
searching through files or hit Return to complete the command.

Showing data values
-------------------

So far we typed ``print x`` to look at the value of ``x``. However, most of the
time for interactive analysis it is faster and better to simply type ``x`` (or
whatever the object name) followed by ``<Return>``. This returns the
“representation” of the object which is often a cleaner and more informative
than the “string” version that gets returned with print. In many cases the
“representation” of an object is the same as Python code to create that object.

Try:

.. sourcecode:: ipython

    In [6]: y = dict((x, 'value is %d' % x**2) for x in range(10))
    
    In [7]: y
    
    In [8]: print y

Reloading modules
-----------------

Suppose you are developing a module, say ``mymodule``, and you want to test the
function ``myfunction`` within that module. First, you need to create a file
named ``mymodule.py`` and create the function::

    def myfunction(argument1):
        output = argument1 / argument2
        return output

First, you need to import the module, and
and then call the function. Of course it will raise a **NameError**, since ``argument2``
is not defined:

.. sourcecode:: ipython
    
    In [9]: import mymodule
    
    In [10]: mymodule.myfunction(5.)
    ---------------------------------------------------------------------------
    NameError                                 Traceback (most recent call last)
    /home/user/workdir/<ipython-input-2-88c3fd4bd2ac> in <module>()
    ----> 1 mymodule.myfunction(5.)
    
    /home/user/workdir/mymodule.py in myfunction(argument1)
             1 def myfunction(argument1):
    ----> 2     output = argument1 / argument2
             3     return output

    NameError: global name 'argument2' is not defined


You need to edit the file and solve the bug. Either open your favorite editor in
another terminal or type

.. sourcecode:: ipython
    
    In [11]: edit mymodule.py

Then, change ``myfunction`` so that the bug is solved::

    def myfunction(argument1,argument2):
        output = argument1 / argument2
        return output

If you now run the above again:

.. sourcecode:: ipython
    
    In [12]: import mymodule
    
    In [13]: mymodule.myfunction(5.)
    ---------------------------------------------------------------------------
    NameError                                 Traceback (most recent call last)
    /home/user/workdir/<ipython-input-2-88c3fd4bd2ac> in <module>()
    ----> 1 mymodule.myfunction(5.)
    
    /home/user/workdir/mymodule.py in myfunction(argument1)
             1 def myfunction(argument1):
    ----> 2     output = argument1 / argument2
             3     return output

    NameError: global name 'argument2' is not defined
    
You see that you end with exactly the same error! The reason for this is that
once a module is loaded, a new ``import`` statement does not reload it again.
Before loading a module, the Python interpreter checks if it already exists in
the local namespace. If it does, the interpreter will simply skip loading the
module. This means that **a module can only be loaded once**. This is valid in
general and is not a restriction of IPython. To force a reload, you can do:

.. sourcecode:: ipython
    
    In [14]: reload(mymodule)
    
    In [15]: mymodule.myfunction(5.,10.)
    Out[15]: 0.5
    
.. warning::
    
    The command ``reload`` is not recursive! To force a reload of **all** modules
    and submodules, you need to import ``deepreload``:
    
    .. sourcecode:: ipython

        In [16]: from IPython.lib.deepreload import reload as dreload
    
        In [17]: dreload(mymodule)
        

Running scripts from the shell
------------------------------

The ``run`` command allows you to run any python script and load all of its data
directly into the interactive namespace. Since the file is re-read from disk each
time, changes you make to it are reflected immediately (unlike imported modules,
which have to be specifically reloaded). You can run existing scripts from the
shell via::

    run myscript.py

Suppose there is a bug in your script and you want to run it again (you can do
``edit myscript.py`` from the script, which will load your favorite editor).
Simply do::

    run myscript.py
    
    
Further reading
---------------

This text is based on, or has elements taken from:

* http://ipython.org/ipython-doc/stable/interactive/reference.html
* http://python4astronomers.github.com/core/ipython.html


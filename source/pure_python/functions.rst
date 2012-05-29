Writing Functions
=================

As with other languages, you can write functions in Python to avoid
repeating code and to improve flow of your programs. Functions use a
similar indented syntax to the loops introduced earlier, with a colon
after the function name and the following lines indented. As with
loops, it is considered good python style to indent with four blank
space. Let's start by defining a simple function::

    def my_function():
        print "Hello World!"
        
This can be called with ``my_function()``. 

.. note:: 
    It is considered good python style to have function names all in
    lower case, with words separated by underscore to improve
    readability.

This is a rather boring function that does not take or return any
arguments. Let's make things a little more complicated::

    def add_two_numbers(x1, x2):
        total = x1 + x2
        return total

This function simply adds the two numbers that it is given as
arguments. As you expect, we can pass integers, floats and strings to
a function. Actually, we can pass *any* Python object, even functions!
Consider the following function::
    
    def print_argument(x=5):
        print x

In this example, we have defined what the default value of the ``x``
variable in the function. This is called a keyword argument. If you
try and call this function without any arguments, the default will be
used. If you call it with an argument, the specified value will be
used.

.. admonition::  Exercise

    Write a function that multiplies the input argument by 7.  If no
    argument is given, it prints 7. If the input argument 6, it
    should print "Answer to the Ultimate Question of Life, The
    Universe, and Everything."

.. raw:: html

    <p class="flip8">Click to Show/Hide Solution</p> <div class="panel8">

::

    def multiply_by_7(x=1):
        if x == 6:
            print ("The meaning of life, the Universe and everything.")
        else:
            print x*7


Functions can also have both keyword and standard arguments::

  >>> def slicer(seq, start=None, stop=None, step=None):
  ...    """ Implement basic Python slicing."""
  ...    return seq[start:stop:step]

  >>> l = [1, 2, 3, 4, 5, 6]
  >>> slicer()
  TypeError: slicer() takes at least 1 argument (0 given)
  >>> slicer(l)
  [1, 2, 3, 4, 5, 6]
  >>> slicer(l, stop=2)
  [1, 2]
  >>> slicer(l, stop=5, step=2)
  [1, 3, 5]

Docstrings
----------

You can use a single string after the first line of a function to
describe what the function does and its parameters. The general
convention is::

  >>> def funcname(params):
  ...	  """Concise one-line sentence describing the function.
  ... 
  ...	  Extended summary which can contain multiple paragraphs.
  ...	  """
  ...	  # function body
  ...	  pass

  >>> help(funcname)

In IPython you can access the same documentation about a function
using ``funcname?`` (Try it now!).

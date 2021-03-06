Control Flow Statements
=======================

Setting and modifying variables will only get you so far before you need to
use control flow statements such as if statements, or loops. This section
describes a few of the most basic control flow statements that you will need
to get started.

``if`` statements
-----------------

The basic syntax for an if-statement is the following::

    if condition:
        # do something
    elif condition:
        # do something else
    else:
        # do yet something else

Notice that there is no statement to end the if statement. Notice also the
presence of a colon (``:``) after each control flow statement. Python relies
on indentation and colons to determine whether it is in a specific block of
code. For example, in the following example::

    if a == 1:
        print "a is 1, changing to 2"
        a = 2
    print "finished"

The first print statement, and the ``a = 2`` statement only get executed if
``a`` is 1. On the other hand, ``print "finished"`` gets executed regardless,
once Python exits the if statement.

.. Note::

    Indentation is very important in Python, and the convention is to
    use four spaces (not tabs) for each level of indent.

Back to the if-statements, the conditions in the statements can be
anything that returns a boolean value. For example, ``a == 1``, ``b !=
4``, and ``c <= 5`` are valid conditions because they return either
``True`` or ``False`` depending on whether the statements are true or
not. Standard comparisons can be used (``==`` for equal, ``!=`` for
not equal, ``<=`` for less or equal, ``>=`` for greater or equal,
``<`` for less than, and ``>`` for greater than), as well as logical
operators (``and``, ``or``, ``not``). Parentheses can be used to
isolate different parts of conditions, to make clear in what order the
comparisons should be executed, for example::

    if (a == 1 and b <= 3) or c > 3:
        # do something

More generally, any function or expression that ultimately returns
``True`` or ``False`` can be used.

Along with comparisons, another commonly-used operator is ``in``. This
is used to test whether an item is contained in any collection::

    >>> b = [1, 2, 3]
    >>> 2 in b
    True
    >>> 5 in b
    False

If `b` is a dictionary, this tests that the item is a key of `b`.

.. Note::

    In the previous examples we have included comments. All lines
    starting with the ``#`` character are ignored by Python. If you
    would like to comment out a section of code, you can enclose it in
    triple quotes: ``'''commented out code'''``.

``for`` loops
-------------

The most common type of loop is the ``for`` loop. In its most basic
form, it is straightforward::

    for value in iterable:
        # do things

The *iterable* can be any Python object that can be iterated
over. This includes lists, tuples, dictionaries, strings. Try the
following in IPython::

    >>> for x in [3, 1.2, 'a']:
    ...     print x
    ...
    3
    1.2
    'a'

Note that by putting the colon at the end of the first line, IPython
automatically knows to indent the next line, so you don't need to
indent it yourself. After typing the ``print`` statement, you need to
press enter twice to tell IPython you are finished writing code.

A common type of for loop is one where the value should go between two
integers with a specific set size. To do this, we can use the
``range`` function. If given a single value, it will give a list
ranging from 0 to the value minus 1::

    >>> range(10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

If given two values, these will be the starting value, and one plus
the ending value::

    >>> range(3, 12)
    [3, 4, 5, 6, 7, 8, 9, 10, 11]

Finally, if a third number is specified, this is taken to be the step size::

    >>> range(2, 20, 2)
    [2, 4, 6, 8, 10, 12, 14, 16, 18]

The ``range`` function can be used as the iterable in a ``for`` loop.

.. admonition::  Exercise

    Write a for loop that prints out the integers 1 to 9, but not 5 and 7.

.. raw:: html

   <p class="flip8">Click to Show/Hide Solution</p> <div class="panel8">

::

    >>> for x in range(1, 10):
    ...    if x != 5 and x != 7:
    ...        print x
    ...
    0
    1
    2
    3
    4
    6
    8
    9

``while`` loops
---------------

Python also provides a ``while`` loop which is similar to a ``for``
loop, but where the number of iterations is defined by a condition
rather than an iterator::

    while condition:
        # do something

For example, in the following example::

    >>> a = 0

    >>> while a < 10:
    ...     print a
    ...     a += 1
    ...
    0
    1
    2
    3
    4
    5
    6
    7
    8
    9

the loop is executed until ``a`` is equal to or exceeds 10.

.. admonition::  Exercise

    Write a while loop to print out the Fibonacci numbers below 100.

.. raw:: html

   <p class="flip9">Click to Show/Hide Solution</p> <div class="panel9">

::

    >>> a = 0
    >>> b = 1
    >>> while a < 100:
    ...     print a
    ...     c = a + b
    ...     a = b
    ...     b = c
    ...
    0
    1
    1
    2
    3
    5
    8
    13
    21
    34
    55
    89

**More advanced features**

``break`` out of enclosing for/while loop::

    >>> z = 1 + 1j
    >>> while abs(z) < 100:
    ...     if z.imag == 0:
    ...         break
    ...     z = z**2 + 1

``continue`` the next iteration of a loop.::

    >>> a = [1, 0, 2, 4]
    >>> for element in a:
    ...     if element == 0:
    ...         continue
    ...     print 1. / element
    ...     
    1.0
    0.5
    0.25

Keeping track of enumeration number
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Common task is to iterate over a sequence while keeping track of the
item number.

* Could use while loop with a counter as above. Or a for loop::


    >>> words = ('cool', 'powerful', 'readable')
    >>> for i in range(0, len(words)):
    ...     print i, words[i]
    ...     
    ...     
    0 cool
    1 powerful
    2 readable

* But Python provides **enumerate** for this::

    >>> for index, item in enumerate(words):
    ...     print index, item
    ...     
    0 cool
    1 powerful
    2 readable


List Comprehensions
-------------------

A common programming structure when assigning values to a list is the
following::

  >>> l = []                      # create the list
  >>> for i in range(10):
  ...    l.append(i**2)

List comprehensions provide a shorter and more readable way of writing
the same loop::

  >>> l = [i**2 for i in range(10)]

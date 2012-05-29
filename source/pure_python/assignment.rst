Assignment operator
===================

`Python library reference
<http://docs.python.org/reference/simple_stmts.html#assignment-statements>`_
says:

  Assignment statements are used to (re)bind names to values and to
  modify attributes or items of mutable objects.

In short, it works as follows (simple assignment):

#. an expression on the right hand side is evaluated, the corresponding
   object is created/obtained
#. a **name** on the left hand side is assigned, or bound, to the
   r.h.s. object

Things to note:

* a single object can have several names bound to it::

   >>> a = [1, 2, 3]
   >>> b = a
   >>> a
   [1, 2, 3]
   >>> b
   [1, 2, 3]
   >>> a is b
   True
   >>> b[1] = 'hi!'
   >>> a
   [1, 'hi!', 3]

* By modifying `b`, we have also modified `a`! This behaviour saves
  the time and memory needed to allocate extra space for a copy of the
  original list. If we want to make a copy, we can explicitly ask
  for one by using the ``list`` command::
  
   >>> a = [1, 2, 3]
   >>> b = list(a)
   >>> b
   [1, 2, 3]
   >>> a is b
   False
   >>> b[1] = 'hi!'
   >>> a
   [1, 2, 3]

* Taking slices of lists does perform a copy::

   >>> a = [1, 2, 3]
   >>> b = a[:2]
   >>> b
   [1, 2]
   >>> b[0] = 'hi!'
   >>> b
   ['hi!', 2]
   >>> a
   [1, 2, 3]

* The key concept here is **mutable vs. immutable**

    * mutable objects can be changed in place
    * immutable objects cannot be modified once created

A very good and detailed explanation of the above issues can be found
in David M. Beazley's article `Types and Objects in Python
<http://www.informit.com/articles/article.aspx?p=453682>`_.

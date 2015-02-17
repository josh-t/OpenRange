
OpenRange
=========

A collection of classes and functions providing some additional tools for arithmetic progressions. 

----

**Classes**: `Range <#range>`_, `RangeList <#rangelist>`_, `EnumRange <#enumrange>`_, `DateRange <#daterange>`_, `DatetimeRange <#datetimerange>`_

**Functions**: `irange <#irange>`_, `range_str <#range_str>`_

----

For more information on the built-in interfaces, see Python 2's `range <https://docs.python.org/2/library/functions.html#range>`_ and `xrange <https://docs.python.org/2/library/functions.html#xrange>`_ functions or Python 3's `range <https://docs.python.org/3/library/stdtypes.html#range>`_ object.

----

Classes
=======

Range
-----

The **Range** class is quite similar in usage to python's built-in ``range`` interface. The first difference you'll notice is that **Range** objects are inclusive of the ``stop`` value.

.. code-block:: python

    >>> from openrange import Range
    >>> for i in Range(0, 10, 2):
    >>>    print i,
    ...
    0 2 4 6 8 10

Another distinguishing characteristic of **Range** objects is that they support floating point values for any of the start, stop, and step values. 

.. code-block:: python

    >>> for i in Range(1, 1.5, .1):
    >>>    print i,
    ...
    1.0 1.1 1.2 1.3 1.4 1.5

* **Range** objects require at least a ``start`` value. The ``stop`` and ``step`` arguments are optional. 

Stringified **Range** objects take the form ``<start>[-<stop>[:<step>]]``.

.. code-block:: python

    >>> r1 = Range(1)
    >>> print r1
    1
    >>> r2 = Range(.1, 1.0)
    >>> print r2
    0.1-1.0
    >>> r3 = Range(1, 10, 2)
    >>> print r3
    1-10:2
    >>> r4 = Range(.1, 1.0, .2)
    >>> print r4
    0.1-1.0:0.2

**Range** objects also support negative step values.

.. code-block:: python

    >>> for i in Range(10, 0, -2):
    ...     print i ,
    ... 
    10 8 6 4 2 0

* See the **irange** convenience function below for a simplified wrapper around **Range** that behaves similarly to the built-in interface.

Signature: ``Range(start, stop, step)``

RangeList
---------

The **RangeList** object is a `mutable sequence <https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types>`_ of **Range** objects. The constructor takes a single required ``ranges_arg`` that can be any of the following types:

* **int** - single integer value
* **float** - single floating point value
* **string** - any valid string represenation of a **Range** or **RangeList**
* **Range** - a single **Range** object
* **RangeList** - another **RangeList** object
* **list** - of any combination of the above types

These types are converted internally to a list of **Range** objects (hence the name). Once constructed, iterating over a **RangeList** object will yield each item in each contained **Range** in the order provided to the constructor. 

.. code-block:: python

    >>> from openrange import RangeList
    >>> for i in  RangeList(["1-10:2", "20-30:5", "25-36:4"]):
    ...     print i,
    ... 
    1 3 5 7 9 20 25 30 25 29 33

.. code-block:: python

It is also possible to iterate over the **Range** objects themselves using the **ranges** property on the object.

.. code-block:: python

    >>> for r in  RangeList(["1-10:2", "20-30:5", "25-36:4"]).ranges:
    ...     for i in r:
    ...         print i,
    ... 
    1 3 5 7 9 20 25 30 25 29 33

The ``compact`` method compacts all contained ranges into the most concise set of ranges possible.

.. code-block:: python

    >>> r = RangeList("1-50:2,25-75:2")
    >>> print r
    1-50:2,25-75:2
    >>> r.compact()
    >>> print r
    1-75:2

The ``first_middle_last`` method returns a tuple of 3 items of the form ``(first, middle, last)`` representing the, you guessed it, first, middle, and last items for all items in the **RangeList**.

.. code-block:: python

    >>> r = RangeList("10-0:-2, 9-10:.1, 1-4:.5")
    >>> r.first_middle_last()
    (10, 9.5, 4.0)

The ``continuous`` method returns True if the **RangeList** has a single contained **Range** and its step is 1.

.. code-block:: python

    >>> r = RangeList("1-10")
    >>> r.continuous
    True
    >>> r = RangeList("1-10, 17-23")
    >>> r.continuous
    False

* An optional ``separator`` can be supplied to the constructor to alter the string representation of the **RangeList** object. 

# TODO: if another separator is supplied to constructor, use that when parsing the ranges_arg.
Signature: ``RangeList(ranges_arg, separator=",")``

DateRange
---------

A subclass of **Range**, the **DateRange** class provides an iterable range of python `date <https://docs.python.org/3/library/datetime.html?highlight=datetime#date-objects>`_ objects.

.. code-block:: python

    >>> from datetime import date, timedelta
    >>> from openrange import DateRange
    >>> d1 = date(2015, 1, 1)
    >>> d2 = date(2016, 1, 1)
    >>> td = timedelta(days=70)
    >>> for d in DateRange(d1, d2, td):
    ...     print d
    ... 
    datetime.date(2015, 1, 1)
    datetime.date(2015, 3, 12)
    datetime.date(2015, 5, 21)
    datetime.date(2015, 7, 30)
    datetime.date(2015, 10, 8)
    datetime.date(2015, 12, 17)
    

The ``step`` argument should be a string of the form ... XXX


Signature: ``DateRange(start, stop, step)``

DatetimeRange
-------------

A subclass of **Range**, the **DatetimeRange** class provides an iterable range of python `datetime <https://docs.python.org/3/library/datetime.html?highlight=datetime#datetime-objects>`_ objects.

.. code-block:: python

# TODO: example

Signature: ``DatetimeRange(start, stop, step)``

Functions
=========

irange
------

Short for 'inclusive range', **irange** is a convenience function that returns an iterable **Range** object. 

.. code-block:: python

    >>> from openrange import irange
    >>> for i in irange(0, 10):
    >>>     print i,
    ...
    0 1 2 3 4 5 6 7 8 9 10
    
    >>> for i in irange(.1, 1, .2):
    >>>     print i,
    ...
    0.1, 0.3, 0.5, 0.7, 0.9

Signature: ``irange(start, stop=None, step=None)``

range_str
---------

The **range_str** function accepts any valid **RangeList** argument and returns a compacted string representation of the supplied ranges. 

.. code-block:: python

    >>> from openrange import range_str
    >>> range_str("1,2,3,4,6,8,10,12")
    '1-4,6-12:2'
    
An optional ``separator`` argument is provided to override the default ``,`` separator.

.. code-block:: python

    >>> from openrange import range_str
    >>> range_str("1,2,3,4,6,8,10,12", separator="|")
    '1-4|6-12:2'

It should be noted that this function removes duplicate items from the supplied range arguments and sorts them in order to determine the compacted string representation.

Signature: ``range_str(ranges_arg, separator=None)``

Support
=======

**OpenRange** has been tested with:

* python 2.6, 2.7, 3.2, 3.3, 3.4, pypy, pypy3

Installation
============

.. code-block:: bash

    $ pip install openrange    <<< not yet

Contribute
==========

Thanks for checking out **OpenRange**! Contribution is welcome from those who propose new features, have ideas for improvement, or submit a bug fixes. Here's a checklist for contributing to this project:

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug. 
#. Fork the repo on GitHub and start making your changes. 
#. Write a test that shows the bug has been fixed or that the feature works as expected.
#. Make sure to add yourself to **CONTRIBUTORS.rst**.
#. Send a pull request.

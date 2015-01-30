
rangetools
==========

A collection of classes and functions providing features not found in python's built-in arithmetic progression interface.

----

For more information on python's built-in interfaces, see:

* `range <https://docs.python.org/2/library/functions.html#range>`_, `xrange <https://docs.python.org/2/library/functions.html#xrange>`_ (Python 2)
* `range <https://docs.python.org/3/library/stdtypes.html#range>`_ (Python 3)

Classes
=======

Range
-----

The **Range** class is quite similar to Python 3's built-in `range <https://docs.python.org/3/library/stdtypes.html#range>`_ object, so its usage should be familiar.

.. code-block:: python

    >>> from rangetools import Range
    >>> for i in Range(0, 10, 2):
    >>>    print str(i),
    0 2 4 6 8 10

* Notice that **Range** objects are inclusive.

A major distinguishing characteristic of **Range** objects is that they support floating point values for any of the start, stop, and step values. 

.. code-block:: python

    >>> for i in Range(1, 1.5, .1):
    >>>    print str(i),
    1.0 1.1 1.2 1.3 1.4 1.5

* **Range** objects require at least a ``start`` value. The ``stop`` and ``step`` arguments are optional. 

Stringified **Range** objects take the form ``<start>[-<stop>[:<step>]]``.

.. code-block:: python

    >>> r1 = Range(1)
    >>> print r1
    1
    >>> r2 = Range(1, 10)
    >>> print r2
    1-10
    >>> r3 = Range(1, 10, 2)
    >>> print r3
    1-10:2
    >>> r4 = Range(.1)
    >>> print r4
    0.1
    >>> r5 = Range(.1, 1.0)
    >>> print r5
    0.1-1.0
    >>> r6 = Range(.1, 1.0, .2)
    >>> print r6
    0.1-1.0:0.2

Two other optional arguments are also available, ``repeat`` and ``continuous``. The ``repeat`` option specifies how many times to iterate over the range. 

.. code-block:: python

    >>> for i in Range(0, 10, 2, repeat=2):
    ...     print(i),
    ... 
    0 2 4 6 8 10 0 2 4 6 8 10

The ``continuous`` option is only valid with the ``repeat`` option and is a boolean value that indicates whether subsequent iterations should begin from the ``start`` value. When set to ``True``, subsequent iterations use the last iterated item plus ``step`` to indicate the new start value. From there, the ``step`` continues as usual for the number of items in the range. This is best illustrated by example.

.. code-block:: python

    >>> for i in Range(0, 10, 2, repeat=2, continuous=True):
    ...     print(i),
    ... 
    0 2 4 6 8 10 12 14 16 18 20 22

* See the **EnumRange** examples below for a better use case for the ``continuous`` option.

**Range** objects also support negative step values and can be used with all of the options shown above.

.. code-block:: python

    >>> for i in Range(10, 0, -2, repeat=2, continuous=True):
    ...     print(i),
    ... 
    10 8 6 4 2 0 -2 -4 -6 -8 -10 -12

* See the **irange** convenience function below for a simplified wrapper around **Range** that behaves similarly to the built-in interface.

Full signature: ``Range(start, stop=None, step=1, repeat=1, continuous=False)``

RangeList
---------

The **RangeList** object is a `mutable sequence <https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types>`_ of **Range** objects. The constructor takes a single required ``ranges_arg`` that can be any of the following types:

* **int** - single integer value
* **float** - single floating point value
* **string** - any valid string represenation of a **Range**, f.e. "1-10:2"
* **Range** - a single **Range** object
* **RangeList** - another **RangeList** object
* **list** - of any combination of the above types

These types are converted internally to a list of **Range** objects (hence the name). Once constructed, iterating over a **RangeList** object will yield each item in each contained **Range** in the order provided to the constructor. 

.. code-block:: python

It is also possible to iterate over the **Range** objects themselves using the **ranges** property on the object.


.. code-block:: python


# TODO: compact, fml, continuous

Full signature: ``RangeList(ranges_arg, separator=",")``

EnumRange
---------

The **EnumRange** class is a subclass of **Range** and provides iterable enumeration of a given sequence. 

.. code-block:: python

    >>> from calendar import day_abbr
    >>> from rangetools import EnumRange
    >>> for d in EnumRange(day_abbr, start="Mon", stop="Sun", step=2):
    ...     print d,
    ... 
    Mon Wed Fri Sun

# TODO: also accepts enumerate object argument to allow non-0 start
# TODO: enumate() method

.. code-block:: python

    >>> for d in EnumRange(day_abbr, start="Mon", stop="Sun", step=2).enumerate():
    ...     print d,
    ... 
    (0, 'Mon') (2, 'Wed') (4, 'Fri') (6, 'Sun')
    >>> e = EnumRange(day_abbr, start="Mon", stop="Sun", step=2)
    >>> print(e)
    Mon-Sun:2
    
The optional ``repeat`` and ``continuous`` arguments available on **Range** can be used as well:

.. code-block:: python

    >>> for d in EnumRange(day_abbr, start="Mon", stop="Sun", step=2, repeat=2, continuous=True):
    ...     print d,
    ... 
    Mon Wed Fri Sun Tue Thu Sat Mon 
    
Full signature: ``EnumRange(sequence, start=None, stop=None, step=1, repeat=None, continuous=False)``

DateRange
---------

A subclass of **Range**, the **DateRange** class provides an iterable range of python `date <https://docs.python.org/3/library/datetime.html?highlight=datetime#date-objects>`_ objects.

.. code-block:: python

    >>> from datetime import date
    >>> from rangetools import DateRange
    >>> d1 = date(2015, 1, 1)
    >>> d2 = date(2016, 1, 1)
    >>> for d in DateRange(d1, d2, step='10w'):
    ...     print str(d),
    ... 
    2014-12-31 2015-03-11 2015-05-20 2015-07-29 2015-10-07 2015-12-16 <<< BUG BUG BUG!!!

The ``step`` argument should be a string of the form ... XXX


Full signature: ``DateRange(start, stop=None, step="1d", repeat=None, continuous=False)``

DatetimeRange
-------------

A subclass of **Range**, the **DatetimeRange** class provides an iterable range of python `datetime <https://docs.python.org/3/library/datetime.html?highlight=datetime#datetime-objects>`_ objects.

.. code-block:: python

# TODO: example

Full signature: ``DatetimeRange(start, stop=None, step="1d", repeat=None, continuous=False)``

Functions
=========

irange
------

Short for 'inclusive range', **irange** is a convenience function that returns an iterable **Range** object. 

.. code-block:: python

    >>> from rangetools import irange
    >>> for i in irange(0, 10):
    >>>     print str(i),
    0 1 2 3 4 5 6 7 8 9 10
    
    >>> for i in irange(.1, 1, .2):
    >>>     print str(i),
    0.1, 0.3, 0.5, 0.7, 0.9

Full signature: ``irange(start, stop=None, step=None)``

range_str
---------

The **range_str** function accepts any valid **RangeList** argument and returns a compacted string representation of the supplied ranges. 

.. code-block:: python

    >>> from rangetools import range_str
    >>> range_str("1,2,3,4,6,8,10,12")
    '1-4,6-12:2'
    
An optional ``separator`` argument is provided to override the default ``,`` separator.

.. code-block:: python

    >>> from rangetools import range_str
    >>> range_str("1,2,3,4,6,8,10,12", separator="|")
    '1-4|6-12:2'

It should be noted that this function removes duplicate items from the supplied range arguments and sorts them in order to determine the compacted string representation.

Full signature: ``range_str(ranges_arg, separator=None)``

Support
=======

**rangetools** has been tested with:

* python 2.7
* pythong 3.???    <<< not yet

Installation
============

.. code-block:: bash

    $ pip install rangetools    <<< not yet

Contribute
==========

Thanks for checking out **rangetools**! Contribution is welcome from those who propose new features, have ideas for improvement, or submit a bug fixes. Here's a checklist for contributing to this project:

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug. 
#. Fork the repo on GitHub and start making your changes. 
#. Write a test that shows the bug has been fixed or that the feature works as expected.
#. Make sure to add yourself to **AUTHORS.rst**.
#. Send a pull request.


rangetools
==========

**rangetools** is a collection of classes and functions providing features not found in python's built-in arithmetic progression interface.

For more information on python's built-in interfaces, see:

* `range <https://docs.python.org/2/library/functions.html#range>`_, `xrange <https://docs.python.org/2/library/functions.html#xrange>`_ (Python 2)
* `range <https://docs.python.org/3/library/stdtypes.html#range>`_ (Python 3)

Classes
=======

Range
-----

The **Range** class is very similar to Python 3's built-in `range <https://docs.python.org/3/library/stdtypes.html#range>`_ object. 

.. code-block:: python

    >>> from rangetools import Range
    >>> for i in Range(0, 10, 2):
    >>>    print str(i),
    0 2 4 6 8 10

.. code-block:: python

    >>> for i in Range(1, 1.5, .1):
    >>>    print str(i),
    1.0 1.1 1.2 1.3 1.4 1.5


# argument defaults...
# string representations...
# continuous
# repeat

See also rangetool's **irange** convenience function.

RangeList
---------

TODO

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
    >>> for d in EnumRange(day_abbr, start="Mon", stop="Sun", step=2).enumerate():
    ...     print d,
    ... 
    (0, 'Mon') (2, 'Wed') (4, 'Fri') (6, 'Sun')
    >>> e = EnumRange(day_abbr, start="Mon", stop="Sun", step=2)
    >>> str(e)
    'Mon-Sun:2'
    
The optional ``repeat`` and ``continuous`` arguments available on **Range** can be used as well:

.. code-block:: python

    >>> for d in EnumRange(day_abbr, start="Mon", stop="Sun", step=2, repeat=2, continuous=True):
    ...     print d,
    ... 
    Mon Wed Fri Sun Tue Thu Sat Mon <<< result is a bug!!! 
    
Full signature: ``EnumRange(sequence, start=None, stop=None, step=1, repeat=None, continuous=False)``

DateRange
---------

TODO

DatetimeRange
-------------

TODO

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

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug. 
#. Fork the repo on GitHub to start making your changes. 
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request.
#. Make sure to add yourself to **AUTHORS.rst** when your changes have been merged into **master**.

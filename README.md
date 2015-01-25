
rangetools
==========

Tools for expanded numerical range processing.


README is a WIP...

Description
===========

Usage
=====

Range
-----

The ``Range`` class provides a reusable, iterable interface to arithmetic
progressions. 

Like the built-in ``range`` function, the ``Range`` object:

- accepts ``start``, ``stop``, and ``step`` values. 

Unlike the built-in ``range`` function, the ``Range`` object:

- allows floating point values
- is inclusive

```python

        >>> # object creation
        >>> from rangetools import Range
        >>> r = Range(0, 10, 2)

        >>> # inclusive iterator
        >>> for i in r:
        >>>    print str(i),
        0 2 4 6 8 10

        >>> # floating point values
        >>> r = Range(1, 1.5, .1)
        >>> for i in r:
        >>>    print str(i),
        1.0 1.1 1.2 1.3 1.4 1.5
```

# argument defaults...
# string representations...


RangeList 
---------

An iterable list of Range objects.

Examples:

irange
------

Similar to the built-in range function, but inclusive. Convenience wrapper
around the Range object, so also supports both integer and floating point
values. 

Examples:

range_str
---------

Examples:

Installation
============

License
=======


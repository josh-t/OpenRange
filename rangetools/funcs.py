"""Functions for expanded numerical range processing."""

from .list_ import RangeList
from .range_ import Range

# ----------------------------------------------------------------------------

__all__ = [
    'irange',
    'range_str',
]

# ----------------------------------------------------------------------------
def irange(start, stop=None, step=None):
    """Similar to the built-in range(), but returns an inclusive iterator.

    >>> from rangetools import irange
    >>> for i in irange(0, 10):
    >>>     print str(i),
    0 1 2 3 4 5 6 7 8 9 10

    """
    return Range(start, stop=stop, step=step)

# ----------------------------------------------------------------------------
def range_str(ranges_arg, separator=None):
    """Given a range argument, return a compacted str representation.

    >>> from rangetools import range_str
    >>> range_str("1,2,3,4,6,8,10,12")
    '1-4,6-12:2'

    Accepts any arguments supported by the RangeList() object. An optional
    'separator' argument can be supplied to override the default subrange
    separator.

    The resulting string is also a valid argument to the RangeList
    constructor.

    """

    range_list = RangeList(ranges_arg, separator=separator)
    range_list.compact()
    return str(range_list)


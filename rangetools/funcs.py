"""Functions for expanded numerical range processing."""

from .base import RangeList
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

# ----------------------------------------------------------------------------
def first_middle_last(items):
    """Given a list of items, return the first, middle, and last item"""

    num_items = 0
    for i in items:
        if num_items == 0:
            first = i
        last = i
        num_items += 1
    
    # calculate the index of the middle item
    if num_items % 2 == 0:
        middle_idx = int(num_items / 2) -1
    else:
        middle_idx = int(num_items / 2)

    count = 0
    for i in items:
        middle = i
        if count == middle_idx:
            break
        count += 1
        
    return (first, middle, last)
        

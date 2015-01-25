"""Classes for expanded numerical range processing."""

# ----------------------------------------------------------------------------

from collections import MutableSequence
from copy import deepcopy
from decimal import Decimal
from itertools import count, groupby
from numbers import Number
import re

# ----------------------------------------------------------------------------

__all__ = [
    'Range',
    'RangeList',
]

# ----------------------------------------------------------------------------

# Optionally signed int or float
NUM_SPEC = "([+-]?(\d+\.?|\d*\.\d+))"

# Range specification
RANGE_SPEC_REGEX = re.compile(
    "^(({i})|({i}-{i})|({i}-{i}:{i}))$".format(i=NUM_SPEC)
)
# Match positions for RANGE_SPEC_REGEX:
#
# 0 = entire match
# 1 = single frame match
# 4 = start-stop (no step) match
# 5 = start if 4
# 7 = stop if 4
# 9 = start-stop:step match
# 10 = start if 9
# 12 = stop if 9
# 14 = step if 9

# A separator regex for parsing a list of range specifications
SPEC_SEPARATOR_REGEX = re.compile("\s*,\s*")

# ----------------------------------------------------------------------------
class Range(object):
    """Iterable, inclusive, numerical range.

    Like the built-in range() function, the Range object provides a way to
    iterate over a list of numbers. Unlike the built-in range() function, the
    Range object supports both integer and float values interchangably.

    Range objects are also inclusive, unlike range().

    Examples:

        >>> rng = Range(0, 10, 2)
        >>> str([i for i in rng])
        '[0, 2, 4, 6, 8, 10]'

        >>> rng = Range(0, 1, .2)
        >>> str([i for i in rng])
        '[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]'

    Negative steps are also supported:

        >>> rng = Range(10, 0, -2)
        >>> str([i for i in rng)
        '[10, 8, 6, 4, 2, 0]'

        >>> rng = Range(1, 0, -.2)
        >>> str([i for i in rng)
        '[1.0, 0.8, 0.6, 0.4, 0.2, 0.0]'

    """

    # ------------------------------------------------------------------------
    def __eq__(self, other):
        """Returns True if the set of items in each list are the same."""
        return set(list(self)) == set(list(other))

    # ------------------------------------------------------------------------
    def __init__(self, start, stop=None, step=1):
        """Constructor.

        raises ValueError if any of start, stop, and step is non numeric

        """

        if stop is None:
            stop = start

        for name, num in [('start', start), ('stop', stop), ('step', step)]:
            if not isinstance(num, Number):
                raise ValueError(
                    "Non-numeric type for '{name}' argument: {t}".format(
                        name=name, t=type(num).__name__))

        self._start = start
        self._stop = stop
        self._step = step

    # ------------------------------------------------------------------------
    def __iter__(self):
        """An iterator for the items in this range.

        Example:

            >>> rng = Range(1, 10, 2)
            >>> for i in rng:
            >>>    print str(i),
            1 3 5 7 9


        """

        # handle all math as decimal operations to avoid floating point
        # precision issues
        (start, stop, step) = \
            [Decimal(str(s)) for s in [self.start, self.stop, self.step]]

        if start == stop:
            yield _str_to_num(str(start))
        else:
            i = start
            num_steps = (stop - start) / step
            for i in range(0, num_steps + 1):
                item = (i * step) + start

                # convert back to float or int from decimal before yielding
                yield _str_to_num(str(item))

    # ------------------------------------------------------------------------
    def __repr__(self):
        return '{cls}("{spec}")'.format(
            cls=self.__class__.__name__, spec=str(self)
        )

    # ------------------------------------------------------------------------
    def __str__(self):
        """Returns a string representation of the range.

        The string returned can vary based on the number of items in the range
        and the step:

            >>> # single value range
            >>> rng = Range(10)
            >>> str(rng)
            "10"

            >>> # step == 1
            >>> rng = Range(1, 10)
            >>> str(rng)
            "1-10"

            >>> # step != 1
            >>> rng = Range(1, 10, 2)
            >>> str(rng)
            "1-10:2"

        """

        (start, stop, step) = \
            [str(s) for s in [self.start, self.stop, self.step]]

        if start == stop:
            spec = start
        else:
            spec = "{start}-{stop}".format(start=start, stop=stop)
            if self.step != 1:
                spec += ":" + step

        return spec

    # ------------------------------------------------------------------------
    @property
    def start(self):
        """The start value for this range."""
        return self._start

    # ------------------------------------------------------------------------
    @property
    def step(self):
        """The step value for this range."""
        return self._step

    # ------------------------------------------------------------------------
    @property
    def stop(self):
        """The stop value for this range."""
        return self._stop

# ----------------------------------------------------------------------------
class RangeList(MutableSequence):
    """An iterable list of Range objects.
    
    This object is represents an iterable list of 1 or more Range objects. To
    instantiate a RangeList object, you can provide a variety of argument types
    to the constructor:

        >>> # single Range object
        >>> rl = RangeList(Range(0, 10, 2)) 

        >>> # Another RangeList object
        >>> r2 = RangeList(r1)

        >>> # single int or float
        >>> r3 = RangeList(99)
        >>> r4 = RangeList(9.9)

        >>> # string specificaiton of a number, Range, or RangeList
        >>> r5 = RangeList("99")
        >>> r6 = RangeList("1-9:3")
        >>> r7 = RangeList("1-9:3,20-30:2")

        >>> # list containing any combination of the above types.
        >>> r8 = RangeList([Range(0, 10, 2), r2, 99, 9.9, "101", "200-300:10"])

    By default, the object iterates over the individual items in each range in
    the list rather than the Range objects themselves:

        >>> rl = RangeList("1-9:3,20-30:2")
        >>> print str([i for i in rl])
        '[1, 4, 7, 20, 22, 24, 26, 28, 30]'

    To iterate over the contained Range objects, use the object's 'ranges'
    property.

    """

    separator = ','

    # ------------------------------------------------------------------------
    def __add__(self, other):
        new_range_list = RangeList(list(self.ranges))
        new_range_list.extend(other)
        return new_range_list

    # ------------------------------------------------------------------------
    def __delitem__(self, index):
        del self._ranges[index]

    # ------------------------------------------------------------------------
    def __init__(self, ranges_arg=None, separator=None):
        """Constructor. 

        raises ValueError if ranges argument is invalid.
        
        """

        self._ranges = []
        self._separator = separator \
            if separator is not None else self.__class__.separator
        if ranges_arg:
            self.extend(ranges_arg)

    # ------------------------------------------------------------------------
    def __getitem__(self, index):
        return self._ranges[index]

    # ------------------------------------------------------------------------
    def __iadd__(self, other):
        self.extend(other)
        return self

    # ------------------------------------------------------------------------
    def __iter__(self):
        for _range in self._ranges:
            for item in _range:
                yield item

    # ------------------------------------------------------------------------
    def __len__(self):
        return len(self._ranges)

    # ------------------------------------------------------------------------
    def __repr__(self):
        return '{cls}("{spec}")'.format(
            cls=self.__class__.__name__, spec=str(self)
        )

    # ------------------------------------------------------------------------
    def __setitem__(self, index, range_arg):
        self._ranges[index] = _arg_to_range(range_arg)

    # ------------------------------------------------------------------------
    def __str__(self):
        return self._separator.join([str(_range) for _range in self._ranges])

    # ------------------------------------------------------------------------
    # methods:
    # ------------------------------------------------------------------------
    def append(self, range_arg):
        """Append a range to the list of ranges."""

        self._ranges.append(_arg_to_range(range_arg))

    # ------------------------------------------------------------------------
    def compact(self):
        """Compact the all contained ranges into most concise set of ranges.

        Example:

            >>> rl = RangeList(["0-10:2", "1-11:2"])
            >>> print str(rl)
            '0-10:2,1-11:2'
            >>> rl.compact()
            >>> print str(rl)
            '0-11'

        WARNING: Running compact() on a RangeList will cause the object to sort
        the contained Range items as well.
 
        """

        self._ranges = _items_to_ranges(list(self))

    # ------------------------------------------------------------------------
    def extend(self, ranges_arg):
        """Extend the list of contained Range objects.
        
        Allowed argument types match the RangeList constructor.

        """
        self._ranges.extend(_arg_to_ranges(ranges_arg))

    # ------------------------------------------------------------------------
    def insert(self, index, range_arg):
        """Insert into the list of contained Range Objects.
        
        Allowed argument type matches the RangeList constructor.

        """
        self._ranges.insert(index, _arg_to_range(range_arg))

    # ------------------------------------------------------------------------
    def pop(self, index):
        """Pop a Range from the list at the given index."""
        return self._ranges.pop(index)

    # ------------------------------------------------------------------------
    def remove(self, range_arg):
        """Remove a specific Range from the list.

        Allowed argument type matches the RangeList constructor.

        """
        self._ranges.remove(_arg_to_range(range_arg))

    # ------------------------------------------------------------------------
    def reverse(self):
        """Reverse the order of the contained Range objects."""
        self._ranges.reverse()

    # ------------------------------------------------------------------------
    # properties
    # ------------------------------------------------------------------------
    @property
    def continuous(self):
        """Returns True if there is one contained Range and its step is 1."""
        return len(self._ranges) == 1 and self._ranges[0].step == 1

    # ------------------------------------------------------------------------
    @property
    def ranges(self):
        """Generates each contained Range object."""
        for _range in self._ranges:
            yield _range

# ----------------------------------------------------------------------------
def _str_to_num(item_str):
    """Converts a given item string into a number.

    Also accepts a default value if the supplied item string is None.


    """

    # Rely on the fact that attempting to convert a string that represents a
    # float in pyhton will raise ValueError.
    try:
        num = int(item_str)
    except ValueError:
        num = float(item_str)

    return num

# ----------------------------------------------------------------------------
def _arg_to_range(range_arg):
    """Convert a single range arg to a Range object."""

    _ranges = _arg_to_ranges(range_arg)

    if len(_ranges) < 1:
        raise ValueError("Could not determine range from: " + str(range_arg))
    elif len(_ranges) > 1:
        raise ValueError("Found multiple ranges for: " + str(range_arg))
    else:
        return _ranges[0]

# ----------------------------------------------------------------------------
def _arg_to_ranges(ranges_arg):
    """Given a supported argument type, convert it into a list of ranges.

    This function takes an argument of unknown but presumably supported type
    and attempts to convert it to a list of ranges.

    """

    ranges = []

    # RangeList
    if isinstance(ranges_arg, RangeList):
        ranges.extend([deepcopy(s) for s in ranges_arg._ranges])

    # Range
    elif isinstance(ranges_arg, Range):
        ranges.append(deepcopy(ranges_arg))

    # string spec
    elif isinstance(ranges_arg, str):
        ranges.extend(_spec_to_ranges(ranges_arg))

    # number
    elif isinstance(ranges_arg, Number):
        ranges.append(Range(ranges_arg))

    # assume a list of one or more of the above types
    else:
        for arg in ranges_arg:
            ranges.extend(_arg_to_ranges(arg))

    return ranges

# ----------------------------------------------------------------------------
def _items_to_ranges(items):
    """Given a list of items, return a full specification string.

    The logic here converts a list of items like:

        [8, 10, 12, 1, 2, 3, 4.5, 5.5, 6.5]

    to a spec string like this:

        "1-3,4.5-6.5,8-10:2"

    It uses an algorithm extrapolated from a simpler case outlined here:

        http://stackoverflow.com/questions/3429510/pythonic-way-to-convert-a-list-of-integers-into-a-string-of-comma-separated-range/3430231#3430231

    The basic idea below is to identify a set of all possible steps between
    the sorted list of items. For example, given a list of items:

        [1, 4, 5, 6, 7, 9, 11]

    The steps would be:

        [3, 1, 1, 1, 2, 2]

    or:

        set(1, 2, 3)

    The code then iterates over each possible step and identifies consecutive
    members of the original list with that step.  To do this it uses a
    combination of itertools.groupby and itertools.count to group consecutive
    items whose offset from a given count is the same.

    Take the example above, starting a count with a step of 2:

        items: [1,  4,  5,  6,  7,   9,  11]
         Count:  0,  2,  4,  6,  8,  10,  12
        Offset: -1, -2, -1,  0,  1,   1,   1]

    The last 3 items, (7, 9, 11), all have the same offset.  A range is
    created for those items with a start of 9, stop of 11, and step of 2.
    These 3 items are removed from the original list and the process continues
    until no more ranges are found.

    The logic only counts 3 or more items as a group and only iterates over
    the possible steps between consecutive items. This implies that there's
    no expectation of maintaining the order of items supplied to this
    function.

    """

    # eliminate duplicates, sort
    items = sorted(list(set(items)))

    # calculate all possible steps between the items
    steps = [items[i] - items[i-1] for i in range(1, len(items))]

    ranges = []

    # only process possible steps
    for step in set(steps):

        # make multiple passes for each step until no ranges are found (3 or
        # more consecutive items with a common step)
        ranges_found = True
        while ranges_found:

            # keep track of how many ranges we find
            num_ranges = 0

            # group the items based on their offset from a matching stepped
            # count. see description in function docs. use str() to allow
            # floating point differences to group properly
            for key, group in groupby(
                items, lambda f,c=count(step=step): str(next(c)-f)):

                range_items = list(group)

                # only count ranges of 3 or more items
                if len(range_items) > 2:
                    num_ranges += 1

                    # create the range
                    ranges.append(Range(
                        range_items[0],
                        stop=range_items[-1],
                        step=step)
                    )

                    # remove the range items from the master list. we're
                    # iterating over this master list and modifying it. it
                    # seems to work, but perhaps there's a case where this
                    # will explode. Someone smart should address this.
                    for i in range_items:
                        items.remove(i)

            ranges_found = True if num_ranges > 0 else False

    # for any remaining items, create single item range.
    for item in items:
        ranges.append(Range(item))

    # return the sorted list of ranges based on the start item
    return sorted(ranges, key=lambda r:r.start)

# ----------------------------------------------------------------------------
def _parse_range_str(range_str):
    """Parse a given range string into (start, stop, and step)

    See comments about match positions where RANGE_SPEC_REGEX is defined.

    """
    
    (start, stop, step) = (None, None, 1)

    match = RANGE_SPEC_REGEX.match(range_str)

    if match:

        groups = match.groups()

        if groups[1] is not None:
            start = groups[1] 
            stop = groups[1]
        elif groups[4] is not None:
            start = groups[5]
            stop = groups[7]
        else:
            start = groups[10] 
            stop = groups[12]
            step = groups[14]

        # convert each to a number
        (start, stop, step) = [_str_to_num(s) for s in [start, stop, step]]

    else:
        raise SyntaxError(
            "Unable to parse range specification: '{s}'".\
                format(s=range_str)
        )

    return (start, stop, step)

# ----------------------------------------------------------------------------
def _spec_to_ranges(spec):
    """Return _Ranges for a given spec string.

    Given a range list specification, split on the separator pattern, then
    parse each individual range. Each range can have a start, stop, and step,
    though only the start is required. Returns a list of _Range objects.

    """

    ranges = []

    for range_str in SPEC_SEPARATOR_REGEX.split(spec):

        (start, stop, step) = _parse_range_str(range_str)
        ranges.append(Range(start, stop=stop, step=step))

    return ranges


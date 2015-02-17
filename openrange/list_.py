
from collections import MutableSequence
from copy import deepcopy
from itertools import chain, count, groupby
from numbers import Number
import re

from .shared import built_in_range

# ----------------------------------------------------------------------------

__all__ = [
    'RangeList',
]

# ----------------------------------------------------------------------------

# Optionally signed int or float
NUM_SPEC = "([+-]?(\d+\.?|\d*\.\d+))"

# Range specification
RANGE_SPEC_REGEX = re.compile(
    "^(({i})|({i}-{i})|({i}-{i}:{i}))$".format(i=NUM_SPEC)
)
# Match positions:
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
        """Initializes a new RangeList.

        Args:
            ranges_arg: May be a RangeList, Range, str, Number, or
                an iterable containing any of the previously mentioned.
            separator(str): The separator to use when splitting the input ranges.
                Default is ','.

        Raises:
            ValueError: If any of the given ranges are of an invalid type.
        """
        self._ranges = []
        self._separator = separator or self.__class__.separator
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
        chain(*self._ranges)

    # ------------------------------------------------------------------------
    def __len__(self):
        return len(self._ranges)

    # ------------------------------------------------------------------------
    def __repr__(self):
        return '{cls}("{spec}")'.format(
            cls=self.__class__.__name__, spec=str(self)
        )

    # ------------------------------------------------------------------------
    def __reversed__(self):
        for _range in reversed(self._ranges):
            for item in reversed(_range):
                yield(item)

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
        """Appends a range to the list of ranges."""
        self._ranges.append(_arg_to_range(range_arg))

    # ------------------------------------------------------------------------
    def compact(self):
        """Compacts all contained ranges into the most concise set of ranges
        possible.

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
    def first_middle_last(self):
        """Returns the first, middle, and last items of the full sequence."""
        # XXX 
        pass

    # ------------------------------------------------------------------------
    def insert(self, index, range_arg):
        """Insert into the list of contained Range Objects.
        
        Allowed argument type matches the RangeList constructor.
        """
        self._ranges.insert(index, _arg_to_range(range_arg))

    # ------------------------------------------------------------------------
    def pop(self, index):
        """Pops a Range from the list at the given index."""
        return self._ranges.pop(index)

    # ------------------------------------------------------------------------
    def remove(self, range_arg):
        """Removes a specific Range from the list.

        Allowed argument type matches the RangeList constructor.
        """
        self._ranges.remove(_arg_to_range(range_arg))

    # ------------------------------------------------------------------------
    def reverse(self):
        """Reverses the order of the contained Range objects in place."""
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
def _arg_to_range(range_arg):
    """Converts a single range arg to a Range object."""
    _ranges = _arg_to_ranges(range_arg)

    if len(_ranges) < 1:
        raise ValueError("Could not determine range from: " + str(range_arg))
    elif len(_ranges) > 1:
        raise ValueError("Found multiple ranges for: " + str(range_arg))
    else:
        return _ranges[0]

# ----------------------------------------------------------------------------
def _arg_to_ranges(ranges_arg):
    """Given a supported argument type, converts it into a list of ranges.

    This function takes an argument of unknown but presumably supported type
    and attempts to convert it to a list of ranges.
    """
    ranges = []

    # RangeList
    if isinstance(ranges_arg, RangeList):
        ranges.extend([deepcopy(s) for s in ranges_arg._ranges])
    elif isinstance(ranges_arg, Range):
        # Range
        ranges.append(deepcopy(ranges_arg))
    elif isinstance(ranges_arg, str):
        # String spec
        ranges.extend(_spec_to_ranges(ranges_arg))
    elif isinstance(ranges_arg, Number):
        # Number
        ranges.append(Range(ranges_arg))
    else:
        # Assume a list of one or more of the above types.
        for arg in ranges_arg:
            ranges.extend(_arg_to_ranges(arg))

    return ranges

# ----------------------------------------------------------------------------
def _items_to_ranges(items):
    """Given a list of items, returns a full specification string.

    The logic here converts a list of items like:

        [8, 10, 12, 1, 2, 3, 4.5, 5.5, 6.5]

    To a spec string like this:

        "1-3,4.5-6.5,8-10:2"

    It uses an algorithm extrapolated from a simpler case outlined here:

        http://stackoverflow.com/questions/3429510/pythonic-way-to-convert-a-list-of-integers-into-a-string-of-comma-separated-range/3430231#3430231

    The basic idea below is to identify a set of all possible steps between
    the sorted list of items. For example, given a list of items:

        [1, 4, 5, 6, 7, 9, 11]

    The steps would be:

        [3, 1, 1, 1, 2, 2]

    Or:

        set(1, 2, 3)

    The code then iterates over each possible step and identifies consecutive
    members of the original list with that step.  To do this it uses a
    combination of itertools.groupby and itertools.count to group consecutive
    items whose offset from a given count is the same.

    Take the example above, starting a count with a step of 2:

         Items: [ 1,  4,  5,  6,  7,  9, 11]
         Count: [ 0,  2,  4,  6,  8, 10, 12]
        Offset: [-1, -2, -1,  0,  1,  1,  1]

    The last 3 items, (7, 9, 11), all have the same offset.  A range is
    created for those items with a start of 9, stop of 11, and step of 2.
    These 3 items are removed from the original list and the process continues
    until no more ranges are found.

    The logic only counts 3 or more items as a group and only iterates over
    the possible steps between consecutive items. This implies that there's
    no expectation of maintaining the order of items supplied to this
    function.
    """
    # Eliminate duplicates and sort.
    items = sorted(list(set(items)))

    # Calculate all possible steps between the items
    steps = [items[i] - items[i-1] for i in built_in_range(1, len(items))]

    ranges = []

    # Only process possible steps.
    for step in set(steps):
        # Make multiple passes for each step until no ranges are found (3 or
        # more consecutive items with a common step).
        ranges_found = True
        while ranges_found:
            # Keep track of how many ranges we find.
            num_ranges = 0

            # Group the items based on their offset from a matching stepped
            # count. See description in function docs. Use str() to allow
            # floating point differences to group properly.
            for key, group in groupby(
                    items, lambda f,c=count(step=step): str(next(c)-f)
                ):

                range_items = list(group)

                # Only count ranges of 3 or more items.
                if len(range_items) > 2:
                    num_ranges += 1

                    # Create the range.
                    ranges.append(Range(
                        range_items[0],
                        stop=range_items[-1],
                        step=step)
                    )

                    # Remove the range items from the master list. We're
                    # iterating over this master list and modifying it. It
                    # seems to work, but perhaps there's a case where this
                    # will explode. Someone smart should address this.
                    for i in range_items:
                        items.remove(i)

            ranges_found = True if num_ranges > 0 else False

    # For any remaining items, create single item range.
    for item in items:
        ranges.append(Range(item))

    # Return the sorted list of ranges based on the start item.
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
        ranges.append(Range(*_parse_range_str(range_str)))

    return ranges


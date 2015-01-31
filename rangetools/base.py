"""Classes for expanded numerical range processing."""

# ----------------------------------------------------------------------------

from collections import Sequence, MutableSequence
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

# ----------------------------------------------------------------------------
# Python 2/3 compatibility
try:
    xrange
except NameError:
    xrange = range

# Optionally signed int or float
NUM_SPEC = "([+-]?(\d+\.?|\d*\.\d+))"

# XXX account for new repeat syntax... wip
#RANGE_SPEC_REGEX = re.compile(
#    "^(({i})(-({i})(:({i}))?)?(x({i}))?)".format(i=NUM_SPEC)
#)

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
# XXX class Range(Sequence):
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
    # XXX document all features

    # ------------------------------------------------------------------------
    def __contains__(self, item):

        (item, start, stop, step) = [
            Decimal(str(i)) for i in [item, self.start, self.stop, self.step]]

        if step > 0:
            if item < start or item > stop:
                return False
        else:
            if item > start or item < stop:
                return False

        return ((item - start) % step) == 0

    # ------------------------------------------------------------------------
    # XXX this the best way?
    def __eq__(self, other):
        """Equals comparator.

        Returns:
            bool: Whether the two objects compare as equal.
        """
        return str(self) == str(other)

    # XXX def __getitem__

    # ------------------------------------------------------------------------
    def __init__(self, start, stop=None, step=1, repeat=1, wrap=False):
        """Initializes a new Range object.

        Args:
            start(numbers.Number): The start number of the range.
            stop(numbers.Number): The end number of the range.  Default is None.
            step(numbers.Number): The step length to use.  Default is 1.
            repeat(int): The number of times to repeat the range.
            wrap(bool): XXX need good explanation

        Raises:
            ValueError: Start, top, or step values are non numeric, or if
                the given repeat value is non-integer or less than 1.
        """
        if stop is None:
            stop = start

        for name, num in [('start', start), ('stop', stop), ('step', step)]:
            if not isinstance(num, Number):
                raise ValueError(
                    "Non-numeric type for '{name}' argument: {t}".format(
                        name=name, t=type(num).__name__))

        if step == 0:
            raise ValueError("Range step cannot be 0.")

        try:
            repeat = int(repeat)
        except ValueError:
            raise ValueError("Repeat argument must be an integer.")

        if repeat < 1:
            raise ValueError("Repeat argument must be positiveinteger.")

        self._repeat = repeat
        self._start = start
        self._stop = stop
        self._step = step
        self._wrap = wrap

    # ------------------------------------------------------------------------
    def __iter__(self):
        """An iterator for the items in this range.

        Example:
            >>> rng = Range(1, 10, 2)
            >>> for i in rng:
            >>>    print str(i),
            1 3 5 7 9
        """
        # Handle all math as decimal operations to avoid floating point
        # precision issues.
        (start, stop, step) = [
            Decimal(str(s)) for s in [
                self.start,
                self.stop,
                self.step,
            ]
        ]

        item = start
        repeats_counter = 1
        while repeats_counter <= self.repeat:
            yield _str_to_num(str(item))
            item += step

            if ((step > 0 and item > stop) or
                (step < 0 and item < stop)):
                repeats_counter += 1
                if self.wrap:
                    if step > 0:
                        item = item - (stop - start + 1)
                    else:
                        item = item + (start - stop + 1) 
                else:
                    item = start


    # XXX def __len__

    # ------------------------------------------------------------------------
    def __repr__(self):
        return '{cls}("{spec}")'.format(
            cls=self.__class__.__name__, spec=str(self)
        )

    # ------------------------------------------------------------------------
    def __reversed__(self):
        new_range = Range(self.start, self.stop, self.step, self.repeat)
        new_range.reverse()
        return new_range

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

            >>> # repeat != 1
            >>> rng = Range(1, 10, 2, 3)
            >>> str(rng)
            "1-10:2x3"
        """
        (start, stop, step) = [
            str(s) for s in [
                self.start,
                self.stop,
                self.step,
            ]
        ]

        if start == stop:
            spec = start
        else:
            spec = "{start}-{stop}".format(start=start, stop=stop)
            if self.step != 1:
                spec += ":" + step

        if self.repeat != 1:
            spec += "x" + str(self.repeat)

        return spec

    # XXX def index

    # XXX def count

    # ------------------------------------------------------------------------
    def first_middle_last(self):
        """Returns the first, middle, and last items of this range."""

        # fast path for a simple range
        if self._step == 1 and isinstance(self._start, int) and \
           isinstance(self._stop, int):
            middle = int((self._start + self._stop) / 2)
            return (self._start, middle, self._stop)

        # slow and sure method
        return _first_middle_last(self)

    # ------------------------------------------------------------------------
    def reverse(self):
        """Reverses the range in place."""
        (self._start, self._stop) = (self._stop, self._start)
        self._step *= -1

    # ------------------------------------------------------------------------
    @property
    def wrap(self):
        """If a repeating range, don't restart the count when repeating."""
        return self._wrap

    # ------------------------------------------------------------------------
    @property
    def repeat(self):
        """The number of repetitions while iterating over this range."""
        return self._repeat

    @repeat.setter
    def repeat(self, repeat):
        if not isinstance(repeat, int):
            raise ValueError('The given repeat value must be of type int.')
        if repeat < 1:
            raise ValueError('The given repeat value must be greater than 0.')
        self._repeat = repeat

    # ------------------------------------------------------------------------
    @property
    def start(self):
        """The start value for this range."""
        return self._start

    @start.setter
    def start(self, start):
        if not isinstance(start, Number):
            raise ValueError('The given start value must be a number.')
        self._start = start

    # ------------------------------------------------------------------------
    @property
    def step(self):
        """The step value for this range."""
        return self._step

    @step.setter
    def step(self, step):
        if not isinstance(step, Number):
            raise ValueError('The given step value must be a number.')
        self._step = step

    # ------------------------------------------------------------------------
    @property
    def stop(self):
        """The stop value for this range."""
        return self._stop

    @stop.setter
    def stop(self, stop):
        if not isinstance(stop, Number):
            raise ValueError('The given stop value must be a number.')
        self._stop = stop

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
            ranges_arg: May be a RangeList, Range, basestring, Number, or
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
        if len(self._ranges) == 1:
            return self._ranges[0].first_middle_last()
        return _first_middle_last(self)

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
def _str_to_num(item_str):
    """Converts a given item string into a number. """
    # Rely on the fact that attempting to convert a string that represents a
    # float in python will raise ValueError.
    try:
        num = int(item_str)
    except ValueError:
        num = float(item_str)
    return num

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
    elif isinstance(ranges_arg, basestring):
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
def _first_middle_last(items):
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
    # Eliminate duplicates and sort.
    items = sorted(list(set(items)))

    # Calculate all possible steps between the items
    steps = [items[i] - items[i-1] for i in xrange(1, len(items))]

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
    # XXX parse the repeat value as well
    
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



# ----------------------------------------------------------------------------
# imports:
# ----------------------------------------------------------------------------

from collections import MutableSequence
from copy import deepcopy
from decimal import Decimal
from itertools import count, groupby
from numbers import Number
import re

# ----------------------------------------------------------------------------
# globals:
# ----------------------------------------------------------------------------

# Optionally signed int or float
ITEM_SPEC = "-?\d*\.?\d*"

# Range specification. Can be a single numeric item or a range of items
# indicated by the '-' separator. An optional step can also be supplied.
RANGE_REGEX = re.compile("^({i})(-?({i})(:({i}))?)?$".format(i=ITEM_SPEC))

# A separator regex for parsing a list of range specifications
SPEC_SEPARATOR_REGEX = re.compile("\s*,\s*")

# ----------------------------------------------------------------------------
# classes:
# ----------------------------------------------------------------------------
class RangeList(MutableSequence):
    """An iterable list of of range specifications."""

    separator = ','

    # ------------------------------------------------------------------------
    # special methods:
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
        return self.items

    # ------------------------------------------------------------------------
    def __len__(self):
        return len(self._ranges)

    # ------------------------------------------------------------------------
    def __setitem__(self, index, range_arg):
        self._ranges[index] = _range_from_arg(range_arg)

    # ------------------------------------------------------------------------
    def __str__(self):
        return self._separator.join([_range.spec for _range in self._ranges])

    # ------------------------------------------------------------------------
    # methods:
    # ------------------------------------------------------------------------
    def append(self, range_arg):
        self._ranges.append(_range_from_arg(range_arg))
    
    # ------------------------------------------------------------------------
    def compact(self):
        self._ranges = _ranges_from_items(list(self.items))

    # ------------------------------------------------------------------------
    def extend(self, ranges_arg):
        self._ranges.extend(_ranges_from_arg(ranges_arg))

    # ------------------------------------------------------------------------
    def insert(self, index, range_arg):
        self._ranges.insert(index, _range_from_arg(range_arg))

    # ------------------------------------------------------------------------
    def pop(self, index):
        return self._ranges.pop(index)

    # ------------------------------------------------------------------------
    def remove(self, range_arg):
        self._ranges.remove(_range_from_arg(range_arg))

    # ------------------------------------------------------------------------
    def reverse(self):
        self._ranges.reverse() 

    # ------------------------------------------------------------------------
    # properties
    # ------------------------------------------------------------------------
    @property
    def continuous(self):
        return len(self._ranges) == 1 and self._ranges[0].step == 1

    # ------------------------------------------------------------------------
    @property
    def ranges(self):
        for _range in self._ranges:
            yield deepcopy(_range)

    # ------------------------------------------------------------------------
    @property
    def items(self):
        for _range in self._ranges:
            for item in _range:
                yield item

# ----------------------------------------------------------------------------
class Range(object):
    # XXX

    # ------------------------------------------------------------------------
    # special methods:
    # ------------------------------------------------------------------------
    def __eq__(self, other):
        """Equality comparison between two Range objects.

        Returns True if the set of items in each list are the same.

        """
        return set(list(self)) == set(list(other))

    # ------------------------------------------------------------------------
    def __init__(self, start, stop=None, step=None):
        """Constructor.

        :raises: ValueError if the step evaluates to False.

        """

        self._start = start
        self._stop = stop if stop is not None else start
        self._step = step if step is not None else 1

        if not self._step:
            raise ValueError("Invalid step: " + self.spec)

    # ------------------------------------------------------------------------
    def __iter__(self):
        """An iterator for the items in this range.

        Example: 

            >>> rng = Range(1, 10, 2)
            >>> for i in rng:
            >>>    print str(i),
            1 3 5 7 9


        """
        return self.items

    # ------------------------------------------------------------------------
    def __str__(self):
        """Returns a string representation of the range.
        
        Example:
            
            >>> rng = Range(1, 20, 2)
            >>> str(rng)
            "1-20:2"

        See also: Range.spec
        
        """

        return self.spec

    # ------------------------------------------------------------------------
    # properties:
    # ------------------------------------------------------------------------
    @property
    def items(self):
        """A generator function that yields all items for this range.
        
        Example:

            >>> rng = Range(1, 10, 2)
            >>> for i in rng.items:
            >>>    print str(i),
            1 3 5 7 9

        See also: Range.__iter__
        
        """

        # handle all math as decimal operations to avoid floating point 
        # precision issues 
        (i, start, stop, step) = map(Decimal, 
            [self.start, self.start, self.stop, self.step])

        if i == stop:
            yield _num_from_str(str(i))
        else:
            num_steps = (stop - start) / step
            for i in range(0, num_steps + 1):
                item = (i * step) + start

                # convert back to float or int from decimal before yielding
                yield _num_from_str(str(item))
            
    # ------------------------------------------------------------------------
    @property
    def spec(self):
        """(str) representation of this range.

        Of the form {start}-{stop}:{step}. If the step is 1, it will not be
        included.

        """

        (start, stop, step) = map(str, [self.start, self.stop, self.step])
        
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
# public functions:
# ----------------------------------------------------------------------------
def irange(start, stop=None, step=None):
    """Similar to the built-in range(), but returns an inclusive iterator.
    
    >>> for i in irange(0, 10):
    >>>     print str(i),
    0 1 2 3 4 5 6 7 8 9 10
    
    """
    return Range(start, stop=stop, step=step)

# ----------------------------------------------------------------------------
# private functions:
# ----------------------------------------------------------------------------
def _num_from_str(item_str, default=None):
    """Converts a given item string into a number.

    Also accepts a default value if the supplied item string is None. 


    """

    if item_str is None:
        return default

    # Rely on the fact that attempting to convert a string that represents a
    # float in pyhton will raise ValueError.
    try:
        num = int(item_str)
    except ValueError:
        num = float(item_str)

    return num

# ----------------------------------------------------------------------------
def _range_from_arg(range_arg):
    """Convert a single range arg to a Range object."""
    
    _ranges = _ranges_from_arg(range_arg)

    if len(_ranges) < 1:
        raise ValueError("Could not determine range from: " + str(range_arg))
    elif len(_ranges) > 1:
        raise ValueError("Found multiple ranges for: " + str(range_arg))
    else:
        return _ranges[0]

# ----------------------------------------------------------------------------
def _ranges_from_arg(ranges_arg):
    """Given a supported argument type, convert it into a list of ranges.

    This function takes an argument of unknown but presumably supported type
    and attempts to convert it to a list of ranges.

    Supported types are:
        
        1. A RangeList object,
        2. A _Range object
        3. A string specificaiton of a RangeList
        4. An int or a float
        5. A list containing any combination of the above types.

    """

    ranges = []

    # RangeList
    if isinstance(ranges_arg, RangeList):
        ranges.extend([deepcopy(s) for s in ranges_arg._ranges])

    # _Range
    elif isinstance(ranges_arg, Range):
        ranges.append(deepcopy(ranges_arg))

    # string spec
    elif isinstance(ranges_arg, basestring):
        ranges.extend(_ranges_from_spec(ranges_arg))

    # number
    elif isinstance(ranges_arg, Number):
        ranges.append(Range(ranges_arg))

    # assume a list of one or more of the above types
    else:
        for arg in ranges_arg:
            ranges.extend(_ranges_from_arg(arg))
        
    return ranges

# ----------------------------------------------------------------------------
def _ranges_from_items(items):
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
def _ranges_from_spec(spec):
    """Return _Ranges for a given spec string.

    Given a range list specification, split on the separator pattern, then
    parse each individual range. Each range can have a start, stop, and step,
    though only the start is required. Returns a list of _Range objects.

    """

    ranges = []

    for range_str in SPEC_SEPARATOR_REGEX.split(spec):

        match = RANGE_REGEX.match(range_str)

        if match:
            
            # make sure each of these has a value. 
            start = _num_from_str(match.group(1))
            stop = _num_from_str(match.group(3), default=start)
            step = _num_from_str(match.group(5), default=1)

            ranges.append(Range(start, stop=stop, step=step))
        else:
            raise SyntaxError(
                "Unable to parse range specification: '{s}'".\
                    format(s=range_str)
            )

    return ranges
        

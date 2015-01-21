
# ----------------------------------------------------------------------------
# imports:
# ----------------------------------------------------------------------------

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
class RangeList(object):
    """Stores an ordered list of numerical items, specified as ranges."""

    separator = ','

    # ------------------------------------------------------------------------
    # special methods:
    # ------------------------------------------------------------------------
    def __add__(self, other):
        new_range_list = RangeList(list(self._ranges))
        new_range_list.add(other) 
        return new_range_list

    # ------------------------------------------------------------------------
    def __init__(self, ranges_arg=None, separator=None):

        self._ranges = []
        self._separator = separator \
            if separator is not None else self.__class__.separator
        if ranges_arg:
            self.add(ranges_arg)

    # ------------------------------------------------------------------------
    def __iter__(self):
        return self.items

    # ------------------------------------------------------------------------
    def __str__(self):
        return self._separator.join([_range.spec for _range in self._ranges])

    # ------------------------------------------------------------------------
    def __sub__(self, other):
        new_range_list = RangeList(list(self._ranges))
        new_range_list.remove(other)
        return new_range_list

    # ------------------------------------------------------------------------
    # methods:
    # ------------------------------------------------------------------------
    def add(self, ranges_arg):
        _ranges = _ranges_from_arg(ranges_arg)
        self._ranges.extend(_ranges)

    # ------------------------------------------------------------------------
    def compact(self):
        self._ranges = _ranges_from_items(list(self.items))

    # ------------------------------------------------------------------------
    def remove(self, ranges_arg):
        updated_ranges = []
        ranges_to_remove = _ranges_from_arg(ranges_arg)
        items_to_remove = list(
            set(_items_from_ranges(ranges_to_remove))
        )
        for _range in self._ranges:
            new_ranges = _Range.remove(_range, items_to_remove)
            if new_ranges:
                updated_ranges.extend(new_ranges)

        self._ranges = updated_ranges

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
            yield RangeList(deepcopy(_range))

    # ------------------------------------------------------------------------
    @property
    def items(self):
        for _range in self._ranges:
            for item in _range:
                yield item

# ----------------------------------------------------------------------------
# private classes:
# ----------------------------------------------------------------------------
class _Range(object):

    # ------------------------------------------------------------------------
    # class methods:
    # ------------------------------------------------------------------------
    @classmethod
    def remove(cls, _range, items_to_remove):

        # XXX remove items from each range individually

        new_ranges = []
        cur_items = list(_range)
        new_items = [i for i in cur_items if not i in items_to_remove]
        return _ranges_from_items(new_items)

    # ------------------------------------------------------------------------
    # special methods:
    # ------------------------------------------------------------------------
    def __init__(self, start, stop=None, step=None):
        self._start = start
        self._stop = stop if stop is not None else start
        self._step = step if step is not None else 1

        if not self._step:
            raise ValueError("Invalid step: " + self.spec)

    # ------------------------------------------------------------------------
    def __iter__(self):
        return self.items

    # ------------------------------------------------------------------------
    def __str__(self):
        return self.spec

    # ------------------------------------------------------------------------
    # properties:
    # ------------------------------------------------------------------------
    @property
    def items(self):
        """A generator function that yields all items for this range."""

        # handle all math as decimal operations to avoid floating point 
        # issues. below, when the item is yielded, it is first converted to
        # a string representation, then to either an int or float. 
        i = Decimal(self.start)
        start = Decimal(self.start)
        stop = Decimal(self.stop)
        step = Decimal(self.step)

        # XXX should be able to do this without conditional

        if i == stop:
            yield _num_from_str(str(i))
        elif stop > start:
            while i <= stop:
                yield _num_from_str(str(i))
                i += step
        else:
            while i >= stop:
                yield _num_from_str(str(i))
                i += step

    # ------------------------------------------------------------------------
    @property
    def spec(self):

        start = str(self.start)
        stop = str(self.stop)
        step = str(self.step)
        
        if start == stop:
            spec = start
        else:
            spec = "{start}-{stop}".format(start=start, stop=stop)
            if step != "1" and step != "1.0":
                spec += ":" + step

        return spec

    # ------------------------------------------------------------------------
    @property
    def start(self):
        return self._start

    # ------------------------------------------------------------------------
    @property
    def step(self):
        return self._step

    # ------------------------------------------------------------------------
    @property
    def stop(self):
        return self._stop

# ----------------------------------------------------------------------------
# private functions:
# ----------------------------------------------------------------------------
def _items_from_ranges(ranges):
    
    items = []
    for _range in ranges:
        items.extend(list(_range))
    return items

# ----------------------------------------------------------------------------
def _num_from_str(item_str, default=None):
    """Converts a given item string into a number.

    Also accepts a default value if the supplied item string is None. 


    """

    if item_str is None:
        return default

    # Rely on the fact that attempting to convert a string that represents a
    # float in pyhton will raise ValueError. This is still not ideal due to 
    # floating point precision problems. 
    try:
        num = int(item_str)
    except ValueError:
        num = float(item_str)

    # TODO: consider use decimal.Decimal for all numbers. Not sure users would
    # want decimal objects returned when iterating over items though. 
    # Somebody smart should propose a good solution.

    return num

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
    elif isinstance(ranges_arg, _Range):
        ranges.append(deepcopy(ranges_arg))

    # string spec
    elif isinstance(ranges_arg, basestring):
        ranges.extend(_ranges_from_spec(ranges_arg))

    # number
    elif isinstance(ranges_arg, Number):
        ranges.append(_Range(ranges_arg))

    # list of one or more of the above types
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
       
        # XXX

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
                    ranges.append(_Range(
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
        ranges.append(_Range(item))

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

            ranges.append(_Range(start, stop=stop, step=step))
        else:
            raise SyntaxError(
                "Unable to parse range specification: '{s}'".\
                    format(s=range_str)
            )

    return ranges
        
# ----------------------------------------------------------------------------
if __name__ == "__main__":

    f1 = RangeList()
    assert str(f1) == ""
    assert f1.continuous == False
    assert list(f1.items) == []
    print str(f1)

    f2 = RangeList("1.0-2.5:.5")
    print str(f2)
    print str(list(f2.items))
    assert str(f2) == "1.0-2.5:0.5"
    assert f2.continuous == False
    assert list(f2.items) == [1.0, 1.5, 2.0, 2.5]

    f3 = RangeList("10-30:2")
    print str(f3)
    assert str(f3) == "10-30:2"
    assert f3.continuous == False
    assert list(f3.items) == [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]

    f4 = RangeList("1-50:2,25-75:2", separator=", ")
    print str(f4)
    f4.compact()
    print str(f4)

    f5 = RangeList("1-100")
    assert f5.continuous == True
    print str(f5)

    f6 = RangeList([1, 2, "1-10:3", "-10-20:5", RangeList("11-33:11"), "2.4-9.6:2.4"])
    print str(f6)
    print str(list(f6.items))

    f7 = f5 - f3
    print str(f7)
    for r in f7.ranges:
        print str(r)
    for r in f7.ranges:
        print str(r)

    f8 = RangeList([1.1, 2.2, 3.3, 4.4, 5.5])
    print str(f8)
    f8.compact()
    print str(f8)


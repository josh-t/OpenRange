"""Create custom arithmetic progression classes."""

# ----------------------------------------------------------------------------

from abc import ABCMeta, abstractmethod
from collections import Sequence
import random

from six import add_metaclass

# ----------------------------------------------------------------------------

try:
    built_in_range = xrange
except NameError:
    built_in_range = range

# ----------------------------------------------------------------------------

__all__ = [
    'BaseRange',
]

# ----------------------------------------------------------------------------
@add_metaclass(ABCMeta)
class BaseRange(Sequence):
    """Abstract base class for custom arithmetic progressions.

    Subclasses need only define how to convert between the type of objects
    within the progression and an underlying numeric type. To do so, these
    abstract methods must be implemented:

        _item_to_num(self, item)
        _num_to_item(self, num)

    In some cases, the step type may differ from the items within the
    progression.  In this case, a subclass should implement the following
    conversion methods:

        _step_to_num(self, step)
        _num_to_step(self, num)

    The default implementations of these step conversion methods assume the
    start, stop, and step are of the same type and therefore call the abstract
    _item_to_num() and _num_to_item() methods. 
    """

    # ------------------------------------------------------------------------
    def __contains__(self, item):
        """Test for inclusion of the supplied item."""

        num = self._item_to_num(item)

        if not self._in_range(num):
            return False

        return ((num - self._start) % self._step) == 0

    # ------------------------------------------------------------------------
    def __eq__(self, other):
        """Test for equality with the supplied object.

        **Note**: This method may require evaluation of all items in each list.
        """

        _len = len(self)
        
        if _len != len(other):
            return False

        for i in built_in_range(0, _len):
            if self[i] != other[i]:
                return False

        return True

    # ------------------------------------------------------------------------
    def __ne__(self, other):
        """Test for inequality with the supplied object.

        **Note**: This method may require evaluation of all items in each list.
        """

        return not self.__eq__(other)

    # ------------------------------------------------------------------------
    def __getitem__(self, index):
        """Retrieves item(s) from the progression for a given index or slice."""

        if isinstance(index, slice):
            return [self._num_to_item(self[i])
                for i in built_in_range(*index.indices(len(self)))]

        elif isinstance(index, int):
            if index < 0:
                index += len(self)
            if index >= len(self):
                raise IndexError(
                    "Index '{i}' is out of range.".format(i=index))

            return self._num_to_item((index * self._step) + self._start)
        else:
            raise TypeError(
                "Invalid index type: {t}".format(t=str(type(index))))

    # ------------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor. Arguments mimic python's built-in range().

        Args:
            start: first item of the progression.
            stop: final item of the progression.
            step: increment item

        Returns:
            BaseRange object.

        Raises:
            TypeError: if args are invalid
            ValueError: if stop value is None
            ValueError: if step is 0
        """

        # default values for start/step
        start = 0
        step = 1

        if len(args) == 1:
            stop = args[0]
        elif len(args) == 2:
            (start, stop) = args
        elif len(args) == 3:
            (start, stop, step) = args
        else:
            raise TypeError(
                "{c} expected at most 3 non-keyword arguments.".format(
                    c=self.__class__.__name__
                )
            )

        step = self._step_to_num(step)

        if stop is None:
            raise ValueError("Stop value cannot be none.")

        if step == 0:
            raise ValueError("Step cannot be 0.")

        self._start = self._item_to_num(start)
        self._stop = self._item_to_num(stop)

        self._step = step

    # ------------------------------------------------------------------------
    def __iter__(self):
        """Generates all items in the progression."""

        for i in self._iter():
            yield self._num_to_item(i)

    # ------------------------------------------------------------------------
    def __len__(self):
        """Returns the length of the progression."""

        return int((self._stop - self._start) / self._step) + 1

    # ------------------------------------------------------------------------
    def __repr__(self):
        """Official string representation of the progression."""

        (start, stop, step) = (self.start, self.stop, self.step)

        rpr = []
        if start != 0 or step != 1:
            rpr.append(start) 

        rpr.append(stop)

        if step != 1:
            rpr.append(step)

        return "{c}({r})".format(
            c=self.__class__.__name__,
            r=", ".join([str(s) for s in rpr]),
        )

    # ------------------------------------------------------------------------
    def __reversed__(self):
        """Returns a new instance with start, stop, and step reversed."""

        cls = self.__class__
        new_range = cls(self.start, self.stop, self.step)
        new_range.reverse()
        return new_range

    # ------------------------------------------------------------------------
    def __str__(self):
        """Informal string representation of the progression."""

        return self.__repr__()
    
    # ------------------------------------------------------------------------
    def index(self, item):
        """Returns the index of the first item matching the supplied item."""

        num = self._item_to_num(item)

        if not self._in_range(num):
            raise ValueError(
                "{i} is not in {c}".format(i=item, c=self.__class__.__name__))
    
        diff = abs(num - self._start)
        if not ((num - self._start) % self._step) == 0:
            raise ValueError(
                "{i} is not in {c}".format(i=item, c=self.__class__.__name__))
            
        return abs(int(diff / self._step))

    # ------------------------------------------------------------------------
    def count(self, item):
        """Returns the number of times item appears in the progression."""

        if self.__contains__(item):
            return 1
        else:
            return 0

    # ------------------------------------------------------------------------
    def enumerate(self, start=0):
        """Generates tuples for each item in the progression.

        The tuples yielded take the form (count, item). Count starts at 0
        unless an optional keyword argument 'start' is supplied with an
        alternate start value.
        """

        count = start
        for item in self:
            yield (count, item)
            count += 1

    # ------------------------------------------------------------------------
    def excluding(self, iterable):
        """Iterate over progression excluding items in supplied iterable."""

        excludes = [self._item_to_num(i) for i in iterable]
        
        for i in self._iter():
            if i not in excludes:
                yield self._num_to_item(i)

    # ------------------------------------------------------------------------
    def repeat(self, times=2):
        """Iterate over the progression multiple times in sequence."""

        if times < 1:
            raise ValueError("Repeat value must be > 1.")
        
        for t in range(times):
            for i in self._iter():
                yield self._num_to_item(i)

    # ------------------------------------------------------------------------
    def random(self):
        """Generate the items in the progression in a random order.
        
        """
        # randomize the indecies, then yield the corresponding item
        for i in random.sample(built_in_range(0, len(self)), len(self)):
            yield self[i]

    # ------------------------------------------------------------------------
    def reverse(self):
        """Reverses the range in place."""
        (self._start, self._stop) = (self._stop, self._start)
        self._step *= -1

    # ------------------------------------------------------------------------
    @property
    def start(self):
        """The start item for this range."""
        return self._num_to_item(self._start)

    # ------------------------------------------------------------------------
    @property
    def step(self):
        """The step item for this range."""
        return self._num_to_step(self._step)

    # ------------------------------------------------------------------------
    @property
    def stop(self):
        """The stop item for this range."""
        return self._num_to_item(self._stop)

    # ------------------------------------------------------------------------
    def _iter(self):
        """Reusable iteration method."""

        i = self._start
        while self._in_range(i):
            yield i
            i += self._step

    # ------------------------------------------------------------------------
    @abstractmethod
    def _item_to_num(self, item):
        """Convert the supplied item to a numerical value."""
       
    # ------------------------------------------------------------------------
    @abstractmethod
    def _num_to_item(self, num):
        """Convert the supplied numerical value to item in the progression."""

    # ------------------------------------------------------------------------
    def _step_to_num(self, step):
        """Convert supplied step item to a numeric value."""
        return self._item_to_num(step)

    # ------------------------------------------------------------------------
    def _num_to_step(self, num):
        """Convert supplied numeric value to a step item."""
        return self._num_to_item(num)


    # ------------------------------------------------------------------------
    def _in_range(self, num):

        if self._step > 0:
            return num >= self._start and num <= self._stop
        else:
            return num <= self._start and num >= self._stop


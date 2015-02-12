
# ----------------------------------------------------------------------------

from abc import ABCMeta, abstractmethod
from collections import Sequence

from six import add_metaclass

from .shared import built_in_range

# ----------------------------------------------------------------------------

__all__ = [
    'BaseRange',
]

# ----------------------------------------------------------------------------
@add_metaclass(ABCMeta)
class BaseRange(Sequence):
    """Abstract base class for custom range objects.

    This class provides an abstract interface to numeric ranges. Subclasses 
    need only define how to convert between the type of objects within the
    range and an underlying numeric type used for iteration.

        _item_to_num()
        _num_to_item()

    In some cases, the step type may differ from the items within the range.
    In this case, a subclass should implement the following conversion methods:

        _step_to_num()
        _num_to_step()

    The default implementations of these step conversion methods assume the
    start, stop, and step are of the same type and therefore call the abstract
    _item_to_num() and _num_to_item() methods. 

    """

    # ------------------------------------------------------------------------
    def __contains__(self, item):
        # XXX

        num = self._item_to_num(item)

        if not self._in_range(num):
            return False

        return ((num - self._start) % self._step) == 0

    # ------------------------------------------------------------------------
    def __eq__(self, other):
        """Equals comparator.

        Returns:
            bool: Whether the two objects compare as equal.

        Start, stop, and step must be the same.

        """
        return self._start == other._start and \
               self._stop == other._stop and \
               self._step == other._step

    # ------------------------------------------------------------------------
    def __getitem__(self, index):
        # XXX

        if isinstance(index, slice):
            return [self._num_to_item(self[i])
                for i in built_in_range(*index.indices(len(self)))]

        elif isinstance(index, int):
            if index < 0:
                index += len(self)
            if index >= len(self):
                raise IndexError("Index '{i}' is out of range.".format(i=index))

            return self._num_to_item((index * self._step) + self._start)
        else:
            raise TypeError(
                "Invalid index type: {t}".format(t=str(type(index)))
            )

    # ------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        # XXX

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

        step = self._item_to_num(step)

        if stop is None:
            raise ValueError("Stop value cannot be none.")

        if step == 0:
            raise ValueError("Step cannot be 0.")

        self._start = self._item_to_num(start)
        self._stop = self._item_to_num(stop)
        self._step = step

        if self._step > 0:
            self._in_range = lambda i: i >= self._start and i <= self._stop
        else:
            self._in_range = lambda i: i <= self._start and i >= self._stop

    # ------------------------------------------------------------------------
    def __iter__(self):
        # XXX

        for i in self._iter():
            yield self._num_to_item(i)

    # ------------------------------------------------------------------------
    def __len__(self):
        # XXX        

        # XXX do this without iterating...
        count = 0
        for i in self:
            count += 1
        
        return count

    # ------------------------------------------------------------------------
    def __repr__(self):
        # XXX
        return '{c}("{r}")'.format(c=self.__class__.__name__, r=str(self))

    # ------------------------------------------------------------------------
    def __reversed__(self):
        # XXX 

        cls = self.__class__
        new_range = cls(self.start, self.stop, self.step)
        new_range.reverse()
        return new_range

    # ------------------------------------------------------------------------
    def __str__(self):
        # XXX 

        # XXX allow empty ranges?

        if self._start == self._stop:
            return self.start
        else:
            rng_str = "{start}-{stop}".format(start=self.start, stop=self.stop)
            if self._step != 1:
                rng_str += ":" + str(self.step)
            return rng_str
        
    # ------------------------------------------------------------------------
    def index(self, value):
        # XXX

        for count, i in self.enumerate():
            if value == i:
                return count

        raise ValueError(
            "{v} is not in {c}".format(v=value, c=self.__class__.__name__)
        )

    # ------------------------------------------------------------------------
    def count(self, value):
        # XXX

        count = 0
        for i in self:
            if value == i:
                count += 1
        
        return count

    # ------------------------------------------------------------------------
    def enumerate(self, start=0):
        # XXX 

        count = start
        for item in self:
            yield (count, item)
            count += 1

    # ------------------------------------------------------------------------
    def excluding(self, iterable):

        excludes = [self._item_to_num(i) for i in iterable]
        
        for i in self._iter():
            if i not in excludes:
                yield self._num_to_item(i)

    # ------------------------------------------------------------------------
    def first_middle_last(self):
        """Returns the first, middle, and last items of this range."""

        mid_index = int(len(self) / 2)
        return (self[0], self[mid_index], self[-1])

    # ------------------------------------------------------------------------
    def repeat(self, times=2):

        if times < 1:
            raise ValueError("Repeat value must be > 1.")
        
        # XXX will this work?
        for t in range(times):
            for i in self._iter():
                yield self._num_to_item(i)

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
        return self._num_to_item(self._step)

    # ------------------------------------------------------------------------
    @property
    def stop(self):
        """The stop item for this range."""
        return self._num_to_item(self._stop)

    # ------------------------------------------------------------------------
    def _iter(self):

        i = self._start
        while self._in_range(i):
            yield i
            i += self._step

    # ------------------------------------------------------------------------
    @abstractmethod
    def _item_to_num(self, item):
        # XXX
        pass
       
    # ------------------------------------------------------------------------
    @abstractmethod
    def _num_to_item(self, num):
        # XXX
        pass

    # ------------------------------------------------------------------------
    def _step_to_num(self, step):
        return self._item_to_num(step)

    # ------------------------------------------------------------------------
    def _num_to_step(self, num):
        return self._num_to_item(num)


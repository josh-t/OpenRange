"""Classes for expanded numerical range processing."""

# ----------------------------------------------------------------------------

from abc import ABCMeta, abstractmethod
from collections import Sequence
from itertools import count

from .shared import first_middle_last as fml

# ----------------------------------------------------------------------------

__all__ = [
    'BaseRange',
]

# ----------------------------------------------------------------------------
class BaseRange(Sequence):
    
    __metaclass__ = ABCMeta

    # ------------------------------------------------------------------------
    def __contains__(self, item):

        item = self.to_num(item)

        if self._step > 0:
            if item < self._start or item > self._stop:
                return False
        else:
            if item > self._start or item < self._stop:
                return False

        return ((item - self._start) % self._step) == 0

    # ------------------------------------------------------------------------
    def __eq__(self, other):
        """Equals comparator.

        Returns:
            bool: Whether the two objects compare as equal.

        Start, stop, step, and repeat must be the same.

        """
        return self.start == other.start and \
               self.stop == other.stop and \
               self.step == other.step and \
               self.repeat == other.repeat

    # ------------------------------------------------------------------------
    def __getitem__(self, index):

        for count, value in self.enumerate():
            if count == index:
                return value

    # ------------------------------------------------------------------------
    def __init__(self, start, stop=None, step=1, repeat=1):
        """Initializes a new Range object.

        Args:
            start(numbers.Number): The start number of the range.
            stop(numbers.Number): The end number of the range.  Default is None.
            step(numbers.Number): The step length to use.  Default is 1.
            repeat(int): The number of times to repeat the range.

        Raises:
            ValueError: Start, stop, or step values are non numeric, or if
                the given repeat value is non-integer or less than 1.
        """
        if start is None:
            raise ValueError("Start value cannot be none.")

        if stop is None:
            stop = start

        if 0 == self.to_num(step):
            raise ValueError("Range step cannot be 0.")

        try:
            if repeat != int(repeat):
                raise ValueError("Repeat argument must be an integer.")
        except ValueError:
            raise ValueError("Repeat argument must be an integer.")

        if repeat < 1:
            raise ValueError("Repeat argument must be positive integer.")

        self.repeat = repeat
        self.start = start
        self.stop = stop
        self.step = step

    # ------------------------------------------------------------------------
    def __iter__(self):
        """An iterator for the items in this range.

        Example:
            >>> rng = Range(1, 10, 2)
            >>> for i in rng:
            >>>    print str(i),
            1 3 5 7 9
        """

        item = self._start
        repeats_counter = 1
        while repeats_counter <= self.repeat:
            yield self.to_value(item)
            item += self._step

            if ((self._step > 0 and item > self._stop) or
                (self._step < 0 and item < self._stop)):
                repeats_counter += 1
                item = self._start

    # ------------------------------------------------------------------------
    def __len__(self):
        
        items = [i for i in self]
        return len(items)

    # ------------------------------------------------------------------------
    def __repr__(self):
        return '{cls}("{spec}")'.format(
            cls=self.__class__.__name__, spec=str(self)
        )

    # ------------------------------------------------------------------------
    def __reversed__(self):
        cls = self.__class__
        new_range = cls(self.start, self.stop, self.step, self.repeat)
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

        if self.start == self.stop:
            spec = str(self.start)
        else:
            spec = "{start}-{stop}".format(start=self.start, stop=self.stop)
            if self.step != 1:
                spec += ":" + str(self.step)

        if self.repeat != 1:
            spec += "x" + str(self.repeat)

        return spec

    # ------------------------------------------------------------------------
    def index(self, value):

        for count, i in self.enumerate():
            if value == i:
                return count

        raise ValueError("{v} is not in this Range".format(v=value))

    # ------------------------------------------------------------------------
    def count(self, value):

        count = 0
        for i in self:
            if value == i:
                count += 1
        
        return count

    # ------------------------------------------------------------------------
    def enumerate(self, start=0):
        c = count(start=start)
        for i in self:
            yield (next(c), i)

    # ------------------------------------------------------------------------
    def first_middle_last(self):
        """Returns the first, middle, and last items of this range."""

        # fast path for a simple range
        if self._step == 1 and isinstance(self._start, int) and \
           isinstance(self._stop, int):
            middle = int((self._start + self._stop) / 2)
            return (self._start, middle, self._stop)

        # slow and sure method
        return fml(self)

    # ------------------------------------------------------------------------
    @abstractmethod
    def to_num(self, value):
        pass
       
    # ------------------------------------------------------------------------
    @abstractmethod
    def to_value(self, num):
        pass

    # ------------------------------------------------------------------------
    def reverse(self):
        """Reverses the range in place."""
        (self._start, self._stop) = (self._stop, self._start)
        self._step *= -1

    # ------------------------------------------------------------------------
    @property
    def repeat(self):
        """The number of repetitions while iterating over this range."""
        return self._repeat

    # ------------------------------------------------------------------------
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
        return self.to_value(self._start)

    # ------------------------------------------------------------------------
    @start.setter
    def start(self, start):
        self._start = self.to_num(start)

    # ------------------------------------------------------------------------
    @property
    def step(self):
        """The step value for this range."""
        return self.to_value(self._step)

    # ------------------------------------------------------------------------
    @step.setter
    def step(self, step):
        self._step = self.to_num(step)

    # ------------------------------------------------------------------------
    @property
    def stop(self):
        """The stop value for this range."""
        return self.to_value(self._stop)

    # ------------------------------------------------------------------------
    @stop.setter
    def stop(self, stop):
        self._stop = self.to_num(stop)


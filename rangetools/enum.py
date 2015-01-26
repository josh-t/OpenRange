
from .base import Range

# ----------------------------------------------------------------------------
class EnumRange(Range):

    def __init__(self, sequence, start=None, stop=None, step=1, repeat=1):

        if isinstance(sequence, enumerate):
            self._sequence = dict(sequence)
        else:
            self._sequence = dict(enumerate(sequence))

        lookup = {v: k for k, v in self._sequence.iteritems()}

        # start
        if start is None:
            start = 0
        else:
            try:
                start = _to_val(start, lookup)
            except ValueError:
                raise ValueError(
                    "Invalid start value for enumerated range: {s}".\
                        format(s=start))

        # stop
        if stop is None:
            stop = len(sequence) - 1
        else:
            try:
                stop = _to_val(stop, lookup)
            except ValueError:
                raise ValueError(
                    "Invalid stop value for enumerated range: {s}".\
                        format(s=stop))
                
        # step
        try:
            step = int(step)
        except:
            ValueError("Step must be 1 for enumerated type.")

        super(EnumRange, self).__init__(
            start, stop=stop, step=step, repeat=repeat)

    # ------------------------------------------------------------------------
    def __iter__(self):

        for i in super(EnumRange, self).__iter__():
            yield self._sequence[i]

    # ------------------------------------------------------------------------
    def __str__(self):

        (start, stop) = \
            [self._sequence[s] for s in [self.start, self.stop]]

        if start == stop:
            spec = start
        else:
            spec = "{start}-{stop}".format(start=start, stop=stop)
            if self.step != 1:
                spec += ":" + str(self.step)

        if self.repeat != 1:
            spec += "x" + str(self.repeat)

        return spec

# ----------------------------------------------------------------------------
def _to_num(val, lookup):

    try:
        num = int(val)
    except ValueError:
        try:
            num = lookup[val]
        except KeyError:
            raise ValueError("Invalid value.")


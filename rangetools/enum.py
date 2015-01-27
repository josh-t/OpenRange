
from .base import Range

# ----------------------------------------------------------------------------
class EnumRange(Range):

    def __init__(self, sequence, start=None, stop=None, step=1, **kwargs):

        if isinstance(sequence, enumerate):
            seq_list = list(sequence)
        else:
            seq_list = list(enumerate(sequence))
            
        self._sequence = dict(seq_list)
        lookup = {v: k for k, v in self._sequence.iteritems()}

        # start
        if start is None:
            start = seq_list[0][0]
        else:
            try:
                start = _to_num(start, lookup)
            except ValueError:
                raise ValueError(
                    "Invalid start value for enumerated range: {s}".\
                        format(s=start))

        # stop
        if stop is None:
            stop = len(seq_list) - 1 + seq_list[0][0]
        else:
            try:
                stop = _to_num(stop, lookup)
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
            start, stop=stop, step=step, **kwargs)

    # ------------------------------------------------------------------------
    def __iter__(self):
        for i in super(EnumRange, self).__iter__():
            i = i % len(self._sequence.keys())
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

    # ------------------------------------------------------------------------
    def enumerate(self):
        for i in super(EnumRange, self).__iter__():
            i = i % len(self._sequence.keys())
            yield i, self._sequence[i]

# ----------------------------------------------------------------------------
def _to_num(val, lookup):

    try:
        num = int(val)
    except ValueError:
        try:
            num = lookup[val]
        except KeyError:
            raise ValueError("Invalid value.")

    return num


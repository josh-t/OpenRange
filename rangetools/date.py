
from datetime import date, datetime
import re

from .base import Range, NUM_SPEC

# TODO:
# there is an issue with negative steps
# docs
# test suite

# ----------------------------------------------------------------------------

__all__ = [
    'DateRange',
    'DatetimeRange',
]

# ----------------------------------------------------------------------------

NUM_SPEC = "([+-]?(\d+\.?|\d*\.\d+))"

# s=seconds, m=minutes, h=hours, d=days, w=weeks, y=years
DELTA_SPEC = re.compile("^{n}([smhdwy])$".format(n=NUM_SPEC))
DELTA_MULTS = {
    's': 1,
    'm': 60,
    'h': 60 * 60,
    'd': 60 * 60 * 24,
    'w': 60 * 60 * 24 * 7,
    'y': 60 * 60 * 24 * 7 * 52,
}

EPOCH = datetime(1970,1,1)

# ----------------------------------------------------------------------------
class _DateTypeRange(Range):

    date_type = None

    # ------------------------------------------------------------------------
    def __init__(self, start, stop=None, step="1d", **kwargs):

        if self.__class__.date_type is None:
            raise NotImplementedError(
                "_DateTypeRange subclass must define 'date_type' attribute."
            )
        
        start = _date_to_seconds(start)
        stop = _date_to_seconds(stop)
        step = _delta_to_seconds(step)

        super(_DateTypeRange, self).__init__(
            start, stop=stop, step=step, **kwargs)

    # ------------------------------------------------------------------------
    def __iter__(self):
        for i in super(_DateTypeRange, self).__iter__():
            fts = getattr(self.__class__.date_type, 'fromtimestamp')
            yield fts(i)

    # ------------------------------------------------------------------------
    # XXX implement __str__ in some reasonable way.

# ----------------------------------------------------------------------------
class DateRange(_DateTypeRange):
    date_type = date

# ----------------------------------------------------------------------------
class DatetimeRange(_DateTypeRange):
    date_type = datetime

# ----------------------------------------------------------------------------
def _date_to_seconds(d):

    if not isinstance(d, (date, datetime)):
        raise ValueError(
            "Can't determine date or datetime from: '{d}'".format(d=d)
        )

    # convert to seconds since epoch
    if isinstance(d, date):
        s = (datetime.combine(d, datetime.min.time()) - EPOCH).total_seconds()
    else:
        s = (d - EPOCH).total_seconds()

    return s

# ----------------------------------------------------------------------------
def _delta_to_seconds(delta):

    if isinstance(delta, str):
        match = DELTA_SPEC.match(delta)
        if not match:
            raise ValueError(
                "Failed to parse delta argument: {d}".format(d=delta)
            )
        (mult, _, mult_type) = match.groups()
        if not mult_type in DELTA_MULTS:
            raise ValueError("Invalid delta type: {t}".format(t=mult_type))
        delta = int(mult) * DELTA_MULTS[mult_type]

    elif isinstance(delta, timedelta):
        delta = timedelta.total_seconds()
    else:
        raise ValueError("Invalid type for 'delta' argument: {t}".format(
            t=type(delta).__name__))

    return delta 
    

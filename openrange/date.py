
from datetime import date, datetime, time
import re
from time import gmtime, localtime, mktime

from .base import BaseRange

# ----------------------------------------------------------------------------

__all__ = [
    'DateRange',
    'DatetimeRange',
    'TimeRange',
]

# ----------------------------------------------------------------------------

NUM_SPEC = "([+-]?(\d+\.?|\d*\.\d+))"

# time variables in seconds
SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY
YEAR = 365 * DAY

DELTA_MULTS = {
    's': SECOND,
    'm': MINUTE,
    'h': HOUR,
    'd': DAY,
    'w': WEEK,
    'y': YEAR,
}

# s=seconds, m=minutes, h=hours, d=days, w=weeks, y=years
DELTA_SPEC = re.compile("^{n}([smhdwy])$".format(n=NUM_SPEC))

# epoch relative to local time
EPOCH = datetime.fromtimestamp(mktime(localtime(0)))

# ----------------------------------------------------------------------------
class _DateTypeRange(BaseRange):

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
    def to_num(self, value):
        # already converted in constructor
        return value

    # ------------------------------------------------------------------------
    def to_value(self, num):
        fts = getattr(self.__class__.date_type, 'fromtimestamp')
        return fts(num)

# ----------------------------------------------------------------------------
class DateRange(_DateTypeRange):
    date_type = date

# ----------------------------------------------------------------------------
class DatetimeRange(_DateTypeRange):
    date_type = datetime

# ----------------------------------------------------------------------------
class TimeRange(BaseRange):

    # ------------------------------------------------------------------------
    def __init__(self, start, stop=None, step="1d", **kwargs):

        start = _time_to_seconds(start)
        stop = _time_to_seconds(stop)
        step = _delta_to_seconds(step)

        # account for day change
        if step > 0 and stop < start:
            stop += DAY
        elif step < 0 and start < stop:
            start += DAY
            
        super(TimeRange, self).__init__(
            start, stop=stop, step=step, **kwargs)

    # ------------------------------------------------------------------------
    def to_num(self, value):
        # already converted in constructor
        return value

    # ------------------------------------------------------------------------
    def to_value(self, num):
        (minutes, seconds) = divmod(num, 60)
        (hours, minutes) = divmod(minutes, 60)
        return time(hours % 24, minutes, seconds)

# ----------------------------------------------------------------------------
def _date_to_seconds(d):

    if not isinstance(d, (date, datetime)):
        raise ValueError(
            "Can't determine date or datetime from: '{d}'".format(d=d)
        )

    # convert to seconds since epoch
    if isinstance(d, datetime):
        s = (d - EPOCH).total_seconds()
    else:
        s = (datetime.combine(d, datetime.min.time()) - EPOCH).total_seconds()

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
    
# ----------------------------------------------------------------------------
def _time_to_seconds(t):

    if isinstance(t, time):
        s = (t.hour * HOUR) + (t.minute * MINUTE) + (t.second * SECOND)
    else:
        raise ValueError("Time value must be of type: 'datetime.time'")

    return s


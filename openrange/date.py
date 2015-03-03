
from datetime import date, datetime, time, timedelta
import re
from time import gmtime, localtime, mktime

from .base import BaseRange

# ----------------------------------------------------------------------------

__all__ = [
    'DateRange',
    'DatetimeRange',
    'TimeRange',
]

# epoch relative to local time
EPOCH = datetime.fromtimestamp(mktime(localtime(0)))

# ----------------------------------------------------------------------------
class _DateTypeRange(BaseRange):
    """Base class for date/datetime range classes."""

    # Set the data type for this object.
    _date_type = None

    # ------------------------------------------------------------------------
    def __init__(self, start, stop, step):
        """Constructor. Start, stop, and step are required."""

        for arg in (start, stop):
            if not isinstance(arg, (date, datetime)):
                raise TypeError(
                    "Invalid type for start/stop argument: '{a}'".\
                        format(a=type(arg).__name__))

        if not isinstance(step, timedelta):
            raise TypeError("Invalid type for step argument: {t}".\
                format(t=type(step).__name__))

        super(_DateTypeRange, self).__init__(start, stop, step)

    # ------------------------------------------------------------------------
    def _item_to_num(self, item):
        """Convert items to seconds since the epoch."""
        
        if isinstance(item, datetime):
            seconds = _delta_to_seconds(item - EPOCH)
        else:
            seconds = _delta_to_seconds(
                datetime.combine(item, datetime.min.time()) - EPOCH)

        return seconds

    # ------------------------------------------------------------------------
    def _num_to_item(self, num):
        """Convert seconds to a date/datetime object."""

        fts = getattr(self.__class__._date_type, 'fromtimestamp')
        return fts(num)

    # ------------------------------------------------------------------------
    def _step_to_num(self, step):
        """Convert timedelta step to seconds."""

        return _delta_to_seconds(step)

    # ------------------------------------------------------------------------
    def _num_to_step(self, num):
        """Convert seconds to timedelta object."""
        
        return timedelta(seconds=num)

# ----------------------------------------------------------------------------
class DateRange(_DateTypeRange):
    """Date object progression."""

    _date_type = date

# ----------------------------------------------------------------------------
class DatetimeRange(_DateTypeRange):
    """Datetime object progression."""

    _date_type = datetime

# ----------------------------------------------------------------------------
class TimeRange(BaseRange):
    """Time object progression."""

    # ------------------------------------------------------------------------
    def __init__(self, start, stop, step):
        """Constructor. Start, stop, and step are required."""

        for arg in (start, stop):
            if not isinstance(arg, time):
                raise TypeError(
                    "Invalid type for start/stop argument: '{a}'".\
                        format(a=type(arg).__name__))

        if not isinstance(step, timedelta):
            raise TypeError("Invalid type for step argument: {t}".\
                format(t=type(step).__name__))

        super(TimeRange, self).__init__(start, stop, step)

        # account for day change
        if self._step > 0 and self._stop < self._start:
            self._stop += _delta_to_seconds(timedelta(days=1))
        elif self._step < 0 and self._start < self._stop:
            self._start += _delta_to_seconds(timedelta(days=1))
            
    # ------------------------------------------------------------------------
    def _item_to_num(self, item):
        """Convert time object to seconds."""

        return _delta_to_seconds(timedelta(hours=item.hour)) + \
               _delta_to_seconds(timedelta(minutes=item.minute)) + \
               _delta_to_seconds(timedelta(seconds=item.second))

    # ------------------------------------------------------------------------
    def _num_to_item(self, num):
        """Convert seconds to time object."""

        (minutes, seconds) = divmod(num, 60)
        (hours, minutes) = divmod(minutes, 60)
        return time(hours % 24, minutes, seconds)

    # ------------------------------------------------------------------------
    def _step_to_num(self, step):
        """Convert timedelta object to seconds."""

        return _delta_to_seconds(step)

    # ------------------------------------------------------------------------
    def _num_to_step(self, num):
        """Convert seconds to timedelta object."""

        return timedelta(seconds=num)

# ----------------------------------------------------------------------------
def _delta_to_seconds(delta):
    """Converts timedelta object to seconds."""

    # using this instead of delta.total_seconds() to support python 2.6
    return int((delta.microseconds + 
        (delta.seconds + delta.days * 24 * 3600) * 10**6) / 10**6)


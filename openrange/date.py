
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
    date_type = None

    # ------------------------------------------------------------------------
    def __init__(self, start, stop, step):
        """Constructor. Start, stop, and step are required."""

        super(_DateTypeRange, self).__init__(start, stop, step)

    # ------------------------------------------------------------------------
    def _item_to_num(self, item):
        """Convert items to seconds since the epoch.
        
        Raises:
            ValueError: If date or datetime can't be determined.
        """
        
        if not isinstance(item, (date, datetime)):
            raise ValueError(
                "Can't determine date or datetime from: '{i}'".format(i=item)
            )

        if isinstance(item, datetime):
            seconds = (item - EPOCH).total_seconds()
        else:
            seconds = (datetime.combine(item, datetime.min.time()) - EPOCH).\
                total_seconds()

        return seconds

    # ------------------------------------------------------------------------
    def _num_to_item(self, num):
        """Convert seconds to a date/datetime object."""

        fts = getattr(self.__class__.date_type, 'fromtimestamp')
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

    date_type = date

# ----------------------------------------------------------------------------
class DatetimeRange(_DateTypeRange):
    """Datetime object progression."""

    date_type = datetime

# ----------------------------------------------------------------------------
class TimeRange(BaseRange):
    """Time object progression."""

    # ------------------------------------------------------------------------
    def __init__(self, start, stop, step):
        """Constructor. Start, stop, and step are required."""

        super(TimeRange, self).__init__(start, stop, step)

        # account for day change
        if self._step > 0 and self._stop < self._start:
            self._stop += _delta_to_seconds(timedelta(days=1))
        elif self._step < 0 and self._start < self._stop:
            self._start += _delta_to_seconds(timedelta(days=1))
            
    # ------------------------------------------------------------------------
    def _item_to_num(self, item):
        """Convert time object to seconds."""

        if not isinstance(item, time):
            raise ValueError("Time value must be of type: 'datetime.time'")

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

    if not isinstance(delta, timedelta):
        raise ValueError("Invalid type for 'delta' argument: {t}".format(
            t=type(delta).__name__))

    return int(delta.total_seconds())
    

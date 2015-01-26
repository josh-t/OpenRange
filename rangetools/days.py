
from .enum import EnumRange

# ----------------------------------------------------------------------------

__all__ = [
    'DaysRange',
    'WeekdaysRange',
]

# ----------------------------------------------------------------------------

WEEKDAYS = [
    "Monday", 
    "Tuesday", 
    "Wednesday", 
    "Thursday",
    "Friday",
]

DAYS = ["Sunday"]
DAYS.extend(WEEKDAYS)
DAYS.append("Saturday")

# ----------------------------------------------------------------------------
class DaysRange(EnumRange):

    def __init__(self, start=None, stop=None, step=1, repeat=1):

        super(DaysRange, self).__init__(
            DAYS, start, stop=stop, step=step, repeat=repeat)

# ----------------------------------------------------------------------------
class WeekdaysRange(EnumRange):

    def __init__(self, start=None, stop=None, step=1, repeat=1):

        super(WeekdaysRange, self).__init__(
            WEEKDAYS, start, stop=stop, step=step, repeat=repeat)


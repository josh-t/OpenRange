
from calendar import day_name, day_abbr, month_name, month_abbr

from .base import BaseRange

# ----------------------------------------------------------------------------

__all__ = [
    'DayRange',
    'MonthRange',
]

# ----------------------------------------------------------------------------
class DayRange(BaseRange):

    # ------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        abbreviate = kwargs.pop('abbreviate', False)

        if abbreviate:
            self._days = list(day_abbr)   
        else:
            self._days = list(day_name)

        super(DayRange, self).__init__(*args, **kwargs)

    # ------------------------------------------------------------------------
    def to_num(self, value):
        try:
            return self._days.index(value)
        except ValueError:
            raise ValueError("Unknown day: '{d}'".format(d=value))
       
    # ------------------------------------------------------------------------
    def to_value(self, num):
        return self._days[num]

    # ------------------------------------------------------------------------
    def step_to_num(self, value):
        return int(value)
       
    # ------------------------------------------------------------------------
    def step_to_value(self, num):
        return num

# ----------------------------------------------------------------------------
class MonthRange(BaseRange):

    # ------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        abbreviate = kwargs.pop('abbreviate', False)

        if abbreviate:
            self._months = list(month_abbr)[1:]   
        else:
            self._months = list(month_name)[1:]

        super(MonthRange, self).__init__(*args, **kwargs)

    # ------------------------------------------------------------------------
    def to_num(self, value):
        try:
            return self._months.index(value)
        except ValueError:
            raise ValueError("Unknown month: '{m}'".format(m=value))
       
    # ------------------------------------------------------------------------
    def to_value(self, num):
        return self._months[num]

    # ------------------------------------------------------------------------
    def step_to_num(self, value):
        return int(value)
       
    # ------------------------------------------------------------------------
    def step_to_value(self, num):
        return num


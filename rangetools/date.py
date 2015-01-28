
from datetime import date, datetime
import re

from .base import Range

# ----------------------------------------------------------------------------

__all__ = [
    'DateRange',
]

# ----------------------------------------------------------------------------

DATETIME_STEP_SPEC = re.compile("^(\d+)([smhdwy])$")

STEP_MULTS = {
    's': 1,
    'm': 60,
    'h': 60 * 60,
    'd': 60 * 60 * 24,
    'w': 60 * 60 * 24 * 7,
    'y': 60 * 60 * 24 * 7 * 52,
}

EPOCH = datetime(1970,1,1)

# ----------------------------------------------------------------------------

class DateRange(Range):

    def __init__(self, start, stop, step, **kwargs):

        # validate start and stop
        for name, d in [('start', start), ('stop', stop)]:
            if not isinstance(d, (date, datetime)):
                raise ValueError(
                    "Invalid type for '{name}' argument: {t}".format(
                        name=name, t=type(d).__name__))
                
        # convert start/stop to seconds since epoch
        start = (datetime.combine(start, datetime.min.time()) - EPOCH).\
            total_seconds()

        stop = (datetime.combine(stop, datetime.min.time()) - EPOCH).\
            total_seconds()

        # step should be timedelta or string
        if isinstance(step, str):
            match = DATETIME_STEP_SPEC.match(step)
            if not match:
                raise ValueError(
                    "Failed to parse 'step' argument: {s}".format(s=step)
                )
            (mult, mult_type) = match.groups()
            if not mult_type in STEP_MULTS:
                raise ValueError("Invalid step type: {t}".format(t=mult_type))
            # XXX allow float mults
            step = int(mult) * STEP_MULTS[mult_type]
        elif isinstance(step, timedelta):
            step = timedelta.total_seconds()
        else:
            raise ValueError("Invalid type for 'step' artument: {t}".format(
                t=type(step).__name__))
        
        super(DateRange, self).__init__(start, stop=stop, step=step, **kwargs)

    def __iter__(self):
        for i in super(DateRange, self).__iter__():
            yield date.fromtimestamp(i)

    def __str__(self):
        # XXX date-date:???x#c?
        pass


#d1 = date(2015, 1, 27)
#d2 = date(2015, 1, 29)
#r = DateRange(d1, d2, step='4h')



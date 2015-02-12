
from pkg_resources import get_distribution, DistributionNotFound

from .ascii_ import AsciiRange
from .base import BaseRange
from .binary import BinaryStrRange
from .calendar_ import DayRange, MonthRange
from .date import DateRange, DatetimeRange, TimeRange
from .enum import EnumRange
from .funcs import irange, range_str
from .list_ import RangeList
from .pow_ import Pow2Range
from .range_ import Range

# ----------------------------------------------------------------------------

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'unknown'


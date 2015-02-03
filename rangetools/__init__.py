
from pkg_resources import get_distribution, DistributionNotFound

from .base import BaseRange
from .collections import RangeDict, RangeList
from .date import DateRange, DatetimeRange, TimeRange
from .enum import EnumRange
from .funcs import irange, range_str
from .range_ import Range

# ----------------------------------------------------------------------------

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'unknown'



from pkg_resources import get_distribution, DistributionNotFound

from .base import Range, RangeDict, RangeList
from .date import DateRange, DatetimeRange
from .enum import EnumRange
from .funcs import irange, range_str

# ----------------------------------------------------------------------------

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'unknown'



from pkg_resources import get_distribution, DistributionNotFound

from .base import BaseRange
from .binary import BinaryStrRange
from .date import DateRange, DatetimeRange, TimeRange
from .funcs import irange, range_str
from .list_ import RangeList
from .range_ import Range

# ----------------------------------------------------------------------------

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'unknown'



from pkg_resources import get_distribution, DistributionNotFound

from .objects import Range, RangeList
from .funcs import irange, range_str

# ----------------------------------------------------------------------------

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'unknown'


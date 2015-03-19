
from pkg_resources import get_distribution, DistributionNotFound

from .base import BaseRange

# ----------------------------------------------------------------------------

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'unknown'


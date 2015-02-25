
from .range_ import Range

# ----------------------------------------------------------------------------

__all__ = [
    'irange',
]

# ----------------------------------------------------------------------------
def irange(*args):
    """Similar to the built-in range(), but returns an inclusive iterator.

    >>> from openrange import irange
    >>> for i in irange(0, 10):
    >>>     print str(i),
    0 1 2 3 4 5 6 7 8 9 10

    Supports int, float, and decimal values.

    """
    return Range(*args)



from decimal import Decimal

from .base import BaseRange

# ------------------------------------------------------------------------

__all__ = [
    'Range',
]

# ------------------------------------------------------------------------
class Range(BaseRange):
    """Iterable, inclusive, numerical range.

    Like the built-in range() function, the Range object provides a way to
    iterate over a list of numbers. Unlike the built-in range() function, the
    Range object supports both integer and float values interchangably.

    Range objects are also inclusive, unlike range().

    Examples:

        >>> rng = Range(0, 10, 2)
        >>> str([i for i in rng])
        '[0, 2, 4, 6, 8, 10]'

        >>> rng = Range(0, 1, .2)
        >>> str([i for i in rng])
        '[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]'

    Negative steps are also supported:

        >>> rng = Range(10, 0, -2)
        >>> str([i for i in rng)
        '[10, 8, 6, 4, 2, 0]'

        >>> rng = Range(1, 0, -.2)
        >>> str([i for i in rng)
        '[1.0, 0.8, 0.6, 0.4, 0.2, 0.0]'
    """

    # ------------------------------------------------------------------------
    def to_num(self, value):

        # Handle all math as decimal operations to avoid floating point
        # precision issues.
        return Decimal(str(value))
       
    # ------------------------------------------------------------------------
    def to_value(self, num):

        num_str = str(num)

        # Rely on the fact that attempting to convert a string that represents
        # a float to an int will raise ValueError
        try:
            value = int(num_str)
        except ValueError:
            value = float(num_str)
    
        return value


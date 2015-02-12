
from decimal import Decimal

from .base import BaseRange

# ------------------------------------------------------------------------

__all__ = [
    'Range',
]

# ------------------------------------------------------------------------
class Range(BaseRange):
    """Generic numerical range.

    Like the built-in range() function, the Range object provides a way to
    iterate over a list of numbers. Unlike the built-in range() function, the
    Range object supports both integer and float values interchangably.

    An ``inclusive()`` method returns an inclusive Range object with the 
    same start, stop, and step values.

    Examples:

        >>> rng = Range(0, 10, 2)
        >>> str([i for i in rng])
        '[0, 2, 4, 6, 8]'

        >>> rng = Range(0, 1, .2)
        >>> str([i for i in rng.inclusive()])
        '[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]'

    Negative steps are also supported:

        >>> rng = Range(1, 0, -.2)
        >>> str([i for i in rng)
        '[1.0, 0.8, 0.6, 0.4, 0.2]'

        >>> rng = Range(1, 0, -.2)
        >>> str([i for i in rng.inclusive())
        '[1.0, 0.8, 0.6, 0.4, 0.2, 0.0]'

    """

    # ------------------------------------------------------------------------
    def _item_to_num(self, item):

        # Handle all math as decimal operations to avoid floating point
        # precision issues.

        return Decimal(str(item))
       
    # ------------------------------------------------------------------------
    def _num_to_item(self, num):

        num_str = str(num)

        # Rely on the fact that attempting to convert a string that represents
        # a float to an int will raise ValueError

        try:
            item = int(num_str)
        except ValueError:
            item = float(num_str)
    
        return item


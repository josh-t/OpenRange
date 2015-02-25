
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
    iterate over a list of numbers. Unlike the built-in range() function, Range
    is an inclusive iterator that supports both integer and float values
    interchangably. 

    Examples:

        >>> rng = Range(0, 1, .2)
        >>> str([i for i in rng])
        '[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]'

    """

    # ------------------------------------------------------------------------
    def _item_to_num(self, item):
        """Converts to Decimal. Try to avoid float precision problems."""

        return Decimal(str(item))
       
    # ------------------------------------------------------------------------
    def _num_to_item(self, num):
        """Convert back to int/float."""

        # Rely on the fact that attempting to convert a string that represents
        # a floating point value to an int will raise ValueError

        num_str = str(num)

        try:
            item = int(num_str)
        except ValueError:
            item = float(num_str)
    
        return item



from decimal import Decimal
from .base import BaseRange

class Range(BaseRange):
    """Inclusive numerical range."""

    def _item_to_num(self, item):
        """Converts to Decimal. Try to avoid float precision problems."""

        return Decimal(repr(item))
       
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


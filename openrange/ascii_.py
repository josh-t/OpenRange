
from .base import BaseRange

# ----------------------------------------------------------------------------

__all__ = [
    'AsciiRange',
]

# ----------------------------------------------------------------------------
class AsciiRange(BaseRange):
    """An iterable range of ascii characters.

    Every 4th lowercase letter, starting with 'a':

        >>> from openrange import AsciiRange
        >>> [a for a in AsciiRange('a', 'z', step=4)]
        ['a', 'e', 'i', 'm', 'q', 'u', 'y']

    Every 5th uppercase letter, starting with 'B':

        >>> [a for a in AsciiRange('B', 'Z', step=5)]
        ['B', 'G', 'L', 'Q', 'V']


    """

    # ------------------------------------------------------------------------
    def to_num(self, value):
        return ord(value)
       
    # ------------------------------------------------------------------------
    def to_value(self, num):
        return chr(num)

    # ------------------------------------------------------------------------
    def step_to_num(self, value):
        return int(value)

    # ------------------------------------------------------------------------
    def step_to_value(self, num):
        return num


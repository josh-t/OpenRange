
from math import log

from .base import BaseRange

# ----------------------------------------------------------------------------

__all__ = [
    'Pow2Range',
]

# ----------------------------------------------------------------------------
class Pow2Range(BaseRange):

    # ------------------------------------------------------------------------
    # XXX __init__  
    # ensure start/stop values are powers of 2

    # ------------------------------------------------------------------------
    def to_num(self, value):

        if value == 1:
            return 0

        try:
            exp = int(log(value) / log(2))
        except ValueError:
            raise ValueError("Value is invalid: {v}".format(v=value))

        if not pow(2, exp) == value:
            raise ValueError("Value is not a power of 2: {v}".format(v=value))
       
        return exp

    # ------------------------------------------------------------------------
    def to_value(self, num):
        return pow(2, num)

    # ------------------------------------------------------------------------
    def step_to_num(self, value):
        return int(value)
       
    # ------------------------------------------------------------------------
    def step_to_value(self, num):
        return num


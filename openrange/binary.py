from .base import BaseRange

# ----------------------------------------------------------------------------

__all__ = [
    'BinaryStrRange',
]

# ----------------------------------------------------------------------------
class BinaryStrRange(BaseRange):

    # ------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        self._padding = kwargs.pop('padding', 0)
        super(BinaryStrRange, self).__init__(*args, **kwargs)

    # ------------------------------------------------------------------------
    def to_num(self, value):
        return int(str(value), 2)
       
    # ------------------------------------------------------------------------
    def to_value(self, num):
        return "{n:b}".format(n=num).zfill(self._padding)


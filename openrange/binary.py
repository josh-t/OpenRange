from .base import BaseRange

# ----------------------------------------------------------------------------

__all__ = [
    'BinaryStrRange',
]

# ----------------------------------------------------------------------------
class BinaryStrRange(BaseRange):

    # ------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        self._padding = len(args[0])
        super(BinaryStrRange, self).__init__(*args, **kwargs)

    # ------------------------------------------------------------------------
    def _item_to_num(self, item):
        return int(str(item), 2)
       
    # ------------------------------------------------------------------------
    def _num_to_item(self, num):
        return "{n:b}".format(n=num).zfill(self._padding)


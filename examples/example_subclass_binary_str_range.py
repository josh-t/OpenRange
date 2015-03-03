#!/usr/bin/env python

from openrange import BaseRange

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

# ----------------------------------------------------------------------------
if __name__ == "__main__":

    for i in BinaryStrRange("1000"):
        print i,

# should print:
# 0000 0001 0010 0011 0100 0101 0110 0111 1000


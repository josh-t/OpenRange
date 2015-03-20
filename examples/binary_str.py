from openrange import BaseRange

class BinaryStrRange(BaseRange):

    def _item_to_num(self, item):
        return int(str(item), 2)
       
    def _num_to_item(self, num):
        return "{n:b}".format(n=num)

for i in BinaryStrRange("1000"):
    print i,

# prints:
# 0 1 10 11 100 101 110 111 1000

from rangetools import *

f1 = RangeList()
assert str(f1) == ""
assert f1.continuous == False
assert list(f1) == []
print str(f1)

f2 = RangeList("1.0-2.5:.5")
print str(f2)
print str(list(f2))
assert str(f2) == "1.0-2.5:0.5"
assert f2.continuous == False
assert list(f2) == [1.0, 1.5, 2.0, 2.5]

f3 = RangeList("10-30:2")
print str(f3)
assert str(f3) == "10-30:2"
assert f3.continuous == False
assert list(f3) == [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]

f4 = RangeList("1-50:2,25-75:2", separator=", ")
print str(f4)
f4.compact()
print str(f4)

f5 = RangeList("1-100")
assert f5.continuous == True
print str(f5)

f6 = RangeList([1, 2, "1-10:3", "-10-20:5", RangeList("11-33:11"), "2.4-9.6:2.4"])
print str(f6)
print str(list(f6))

f7 = f3 + f5
print str(f7)

f8 = RangeList([1.1, 2.2, 3.3, 4.4, 5.5])
print str(f8)
f8.compact()
print str(f8)
print range_str(f8)

f9 = RangeList("10-1:-1")
print str(f9)
print str(list(f9))

print range_str([1.1, 2.2, 3.3, 4.4, 5.5])
print range_str("1.1-5.5:1.1")

r1 = RangeList(Range(0, 10, 2)) 
print str(r1)
r2 = RangeList(r1)
print str(r2)
r3 = RangeList(99)
print str(r3)
r4 = RangeList(9.9)
print str(r4)
r5 = RangeList("99")
print str(r5)
r6 = RangeList("1-9:3")
print str(r6)
r7 = RangeList("1-9:3,20-30:2")
print str(r7)
r8 = RangeList([Range(0, 10, 2), r2, 99, 9.9, "101", "200-300:10"])
print str(r8)

rl = RangeList("1-9:3,20-30:2")
print str([i for i in rl])

rl = RangeList(["0-10:2", "1-11:2"])
print str(rl)
rl.compact()
print str(rl)


import unittest
from rangetools import Range

class TestRange(unittest.TestCase):
    def setUp(self):
        pass

    def test_range_args(self):
        # non numeric argument
        args = [None]
        self.assertRaises(ValueError, Range, *args)

        # step cannot be 0
        args = [1,1,0]
        self.assertRaises(ValueError, Range, *args)

        # repeat must be integer
        args = [1,2,1]
        kwargs = {'repeat': 1.5}
        self.assertRaises(ValueError, Range, *args, **kwargs)

        # repeat must be greater than or equal to 1
        args = [1,2,1]
        kwargs = {'repeat': -0.5}
        self.assertRaises(ValueError, Range, *args, **kwargs)

    def test_basic_range(self):
        # Only start argument
        rng = Range(2.3)
        items = [x for x in rng]
        self.assertEquals(items, [2.3])

        # start equals stop
        rng = Range(-1.3, -1.3)
        items = [x for x in rng]
        self.assertEquals(items, [-1.3])

        # integer start integer stop, ascending step by one
        rng = Range(0,2,1)
        items = [x for x in rng]
        self.assertEquals(items, [0, 1, 2])

        # integer start float stop, ascending step by one
        rng = Range(-1, .5, 1)
        items = [x for x in rng]
        self.assertEquals(items, [-1, 0])

        # float start float stop, ascending step by one
        rng = Range(.5, 2.5, 1)
        items = [x for x in rng]
        self.assertEquals(items, [0.5, 1.5, 2.5])

        # float step
        rng = Range(1, 2, .3)
        items = [x for x in rng]
        self.assertEquals(items, [1, 1.3, 1.6, 1.9])

        # negative float step
        rng = Range(10, 8.5, -0.5)
        items = [x for x in rng]
        self.assertEquals(items, [10, 9.5, 9.0, 8.5])

        # First step is outside bounds.
        rng = Range(0, 1, -1)
        items = [x for x in rng]
        self.assertEquals(items, [0])


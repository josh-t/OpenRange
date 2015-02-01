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

    def test_range_wrap(self):
        # Integer step wrap
        rng = Range(0, 2, 1, repeat=2, wrap=True)
        items = [x for x in rng]
        self.assertEquals(items, [0, 1, 2, 0, 1, 2])

        # Float step wrap
        rng = Range(0, 1, .4, repeat=2, wrap=True)
        items = [x for x in rng]
        self.assertEquals(items, [0, 0.4, 0.8, 0.2, 0.6, 1.0])

        # all float wrap, descending step hits start
        rng = Range(10.1, 9.3, -.2, repeat=2, wrap=True)
        items = [x for x in rng]
        self.assertEquals(items, [10.1, 9.9, 9.7, 9.5, 9.3, 9.9, 9.7, 9.5, 9.3])

        # all float wrap, descending step does not hit start
        rng = Range(10.1, 9.3, -.3, repeat=2, wrap=True)
        items = [x for x in rng]
        self.assertEquals(items, [10.1, 9.8, 9.5, 10.0, 9.7, 9.4])

    def test_ridiculous(self):
        # ridiculous arguments ... need to determine what should happen here
        rng = Range(0,0.1,1000, repeat=2, wrap=True)
        items = [x for x in rng]
        self.assertEquals(True, False)

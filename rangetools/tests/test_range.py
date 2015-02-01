import unittest
import rangetools

class TestRange(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic_range(self):
        # integer start integer stop, ascending step by one
        rng = rangetools.Range(0,2,1)
        items = [x for x in rng]
        self.assertEquals(items, [0, 1, 2])

        # integer start float stop, ascending step by one
        rng = rangetools.Range(-1, .5, 1)
        items = [x for x in rng]
        self.assertEquals(items, [-1, 0])

        # float start float stop, ascending step by one
        rng = rangetools.Range(.5, 2.5, 1)
        items = [x for x in rng]
        self.assertEquals(items, [0.5, 1.5, 2.5])

        # First step is outside bounds.
        rng = rangetools.Range(0, 1, -1)
        items = [x for x in rng]
        self.assertEquals(items, [0])

    def test_range_wrap(self):
        rng = rangetools.Range(0, 2, 1, repeat=2, wrap=True)
        items = [x for x in rng]
        self.assertEquals(items, [0, 1, 2, 0, 1, 2])

        rng = rangetools.Range(0, 1, .4, repeat=2, wrap=True)
        items = [x for x in rng]
        self.assertEquals(items, [0, 0.4, 0.8, 0.2, 0.6, 1.0])

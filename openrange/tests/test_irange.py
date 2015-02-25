import unittest
from openrange import irange

class TestIRange(unittest.TestCase):

    def setUp(self):
        pass

    # __init__ tests

    def test_start_none(self):
        self.assertRaises(ValueError, irange, None)

    def test_step_0(self):
        self.assertRaises(ValueError, irange, 1, 1, 0)

    # __iter__ tests

    def test_stop_only_empty(self):
        rng = irange(0)
        items = [x for x in rng]
        self.assertEqual(items, [0])

    def test_stop_only(self):
        rng = irange(3)
        items = [x for x in rng]
        self.assertEqual(items, [0, 1, 2, 3])

    def test_stop_only_float(self):
        rng = irange(2.3)
        items = [x for x in rng]
        self.assertEqual(items, [0, 1, 2])

    def test_same_start_stop_int(self):
        rng = irange(7, 7)
        items = [x for x in rng]
        self.assertEqual(items, [7])

    def test_same_start_stop_float(self):
        rng = irange(-1.3, -1.3)
        items = [x for x in rng]
        self.assertEqual(items, [-1.3])

    def test_ascending_step_1(self):
        rng = irange(0,2,1)
        items = [x for x in rng]
        self.assertEqual(items, [0, 1, 2])

    def test_ascending_int_start_float_stop(self):
        rng = irange(-1, .5, 1)
        items = [x for x in rng]
        self.assertEqual(items, [-1, 0])

    def test_float_ascending_int_step(self):
        rng = irange(.5, 2.5, 1)
        items = [x for x in rng]
        self.assertEqual(items, [0.5, 1.5, 2.5])

    def test_int_ascending_float_step(self):
        rng = irange(1, 2, .3)
        items = [x for x in rng]
        self.assertEqual(items, [1, 1.3, 1.6, 1.9])

    def test_descending_float_step(self):
        rng = irange(10, 8.5, -0.5)
        items = [x for x in rng]
        self.assertEqual(items, [10, 9.5, 9.0, 8.5])

    def test_step_opposite_direction(self):
        rng = irange(0, 1, -1)
        items = [x for x in rng]
        self.assertEqual(items, [])

    # __contains__ tests

    def test_contains_int(self):
        rng = irange(0, 10, 2)
        self.assertTrue(4 in rng)
        self.assertFalse(5 in rng)
        self.assertFalse(-1 in rng)
        self.assertFalse(11 in rng)

    def test_contains_float(self):
        rng = irange(.1, 1.1, .2)
        self.assertTrue(.5 in rng)
        self.assertFalse(.6 in rng)
        self.assertFalse(.05 in rng)
        self.assertFalse(1.2 in rng)

    # __eq__ tests

    def test_equals(self):
        rng1 = irange(0, 10, 2)
        rng2 = irange(0, 10, 2)
        rng3 = irange(0.0, 10.0, 2.0)
        rng4 = irange(0.1, 10, 2.0)
        rng5 = irange(10, 0, -2)
        self.assertTrue(rng1 == rng2)
        self.assertTrue(rng1 == rng3)
        self.assertFalse(rng1 == rng4)
        self.assertFalse(rng1 == rng5)
        
    # __repr__ tests

    def test_int_repr(self):
        rng = irange(0, 10, 2)
        self.assertEqual(repr(rng), 'Range("0-10:2")')

    def test_float_repr(self):
        rng = irange(0.1, 1., 2.)
        self.assertEqual(repr(rng), 'Range("0.1-1.0:2.0")')

    def test_mixed_repr(self):
        rng = irange(0.1, 10, 2.)
        self.assertEqual(repr(rng), 'Range("0.1-10:2.0")')


    # __str__ tests

    def test_single_int_str(self):
        rng = irange(1)
        self.assertEqual(str(rng), "0-1")

    def test_default_step_str(self):
        rng = irange(1, 10)
        self.assertEqual(str(rng), "1-10")

    def test_int_str(self):
        rng = irange(0, 10, 2)
        self.assertEqual(str(rng), "0-10:2")

    def test_float_str(self):
        rng = irange(0.1, 1., 2.)
        self.assertEqual(str(rng), "0.1-1.0:2.0")

    def test_mixed_str(self):
        rng = irange(0.1, 10, 2.)
        self.assertEqual(str(rng), "0.1-10:2.0")

    # enumerate tests

    def test_enumerate_int(self):
        rng = irange(0, 4, 2)
        items = [i for i in rng.enumerate()]
        self.assertEqual(items, [(0, 0), (1, 2), (2, 4)])

    def test_enumerate_float(self):
        rng = irange(0, .4, .2)
        items = [i for i in rng.enumerate()]
        self.assertEqual(items, [(0, 0), (1, .2), (2, .4)])

    # first_middle_last tests

    def test_single_int_range(self):
        rng = irange(42)
        self.assertEqual(rng.first_middle_last(), (0, 21, 42))

    def test_int_range(self):
        rng = irange(0, 4, 2)
        self.assertEqual(rng.first_middle_last(), (0, 2, 4))

    def test_float_range(self):
        rng = irange(0, .4, .2)
        self.assertEqual(rng.first_middle_last(), (0, .2, .4))

    def test_int_range_even_number_of_items(self):
        rng = irange(0, 10, 2)
        self.assertEqual(rng.first_middle_last(), (0, 6, 10))

    # reverse tests

    def test_int_asc_to_desc(self):
        rng = irange(0, 10, 2)
        rng.reverse()
        self.assertEqual(rng.start, 10)
        self.assertEqual(rng.stop, 0)
        self.assertEqual(rng.step, -2)

    def test_int_desc_to_asc(self):
        rng = irange(10, 0, -2)
        rng.reverse()
        self.assertEqual(rng.start, 0)
        self.assertEqual(rng.stop, 10)
        self.assertEqual(rng.step, 2)

    def test_float_asc_to_desc(self):
        rng = irange(0, 1.0, .2)
        rng.reverse()
        self.assertEqual(rng.start, 1.0)
        self.assertEqual(rng.stop, 0)
        self.assertEqual(rng.step, -.2)

    def test_float_desc_to_asc(self):
        rng = irange(1.0, 0, -.2)
        rng.reverse()
        self.assertEqual(rng.start, 0)
        self.assertEqual(rng.stop, 1.0)
        self.assertEqual(rng.step, .2)

    # property getter tests

    def test_int_range_properties_get(self):
        rng = irange(0, 10, 2)
        self.assertTrue(isinstance(rng.start, int))
        self.assertEqual(rng.start, 0)
        self.assertTrue(isinstance(rng.stop, int))
        self.assertEqual(rng.stop, 10)
        self.assertTrue(isinstance(rng.step, int))
        self.assertEqual(rng.step, 2)

    def test_float_range_properties_get(self):
        rng = irange(0.1, 1.0, .2)
        self.assertTrue(isinstance(rng.start, float))
        self.assertEqual(rng.start, 0.1)
        self.assertTrue(isinstance(rng.stop, float))
        self.assertEqual(rng.stop, 1.0)
        self.assertTrue(isinstance(rng.step, float))
        self.assertEqual(rng.step, .2)

    # __getitem__ tests

    def test_int_range_indexing(self):
        rng = irange(1, 10, 2)
        self.assertEqual(rng[0], 1)
        self.assertEqual(rng[1], 3)
        self.assertEqual(rng[2], 5)
        self.assertEqual(rng[3], 7)
        self.assertEqual(rng[4], 9)

    def test_float_range_indexing(self):
        rng = irange(.1, 1.0, .2)
        self.assertEqual(rng[0], .1)
        self.assertEqual(rng[1], .3)
        self.assertEqual(rng[2], .5)
        self.assertEqual(rng[3], .7)
        self.assertEqual(rng[4], .9)

    # XXX negative indexes, slice objects

    # __len__ tests

    def test_len_single(self):
        rng = irange(32)
        self.assertEqual(len(rng), 33)

    def test_len(self):
        rng = irange(0, 10, 2)
        self.assertEqual(len(rng), 6)

    def test_len_float_step(self):
        rng = irange(1, 3, .23)
        self.assertEqual(len(rng), 9)

    def test_len_negative_step(self):
        rng = irange(.9, .27, -.08)
        self.assertEqual(len(rng), 8)

    # index tests

    def test_index_int(self):
        rng = irange(0, 10, 2)
        self.assertEqual(rng.index(4), 2)

    def test_index_float(self):
        rng = irange(0, 1.0, .2)
        self.assertEqual(rng.index(.4), 2)

    def test_index_negative_step(self):
        rng = irange(3.7, 1.2, -.3)
        self.assertEqual(rng.index(3.1), 2)

    def test_not_in_range(self):
        rng = irange(0, 10, 2)
        self.assertRaises(ValueError, rng.index, 1)
        self.assertRaises(ValueError, rng.index, -1)
        self.assertRaises(ValueError, rng.index, 11)

    # count tests

    def test_count_simple(self):
        rng = irange(0, 10, 2)
        self.assertEqual(rng.count(4), 1)


import unittest
from rangetools import Range

class TestRange(unittest.TestCase):

    def setUp(self):
        pass

    # __init__ tests

    def test_start_none(self):
        args = [None]
        self.assertRaises(ValueError, Range, *args)

    def test_step_0(self):
        args = [1, 1]
        kwargs = {'step': 0}
        self.assertRaises(ValueError, Range, *args, **kwargs)

    def test_repeat_non_int(self):
        args = [1,2,1]
        kwargs = {'repeat': 1.5}
        self.assertRaises(ValueError, Range, *args, **kwargs)

    def test_repeat_not_zero(self):
        args = [1,2,1]
        kwargs = {'repeat': 0}
        self.assertRaises(ValueError, Range, *args, **kwargs)

    # __iter__ tests

    def test_single_int(self):
        rng = Range(2)
        items = [x for x in rng]
        self.assertTrue(isinstance(items[0], int))
        self.assertEqual(items, [2])

    def test_single_float(self):
        rng = Range(2.3)
        items = [x for x in rng]
        self.assertTrue(isinstance(items[0], float))
        self.assertEqual(items, [2.3])

    def test_same_start_stop_int(self):
        rng = Range(7, 7)
        items = [x for x in rng]
        self.assertTrue(isinstance(items[0], int))
        self.assertEqual(items, [7])

    def test_same_start_stop_float(self):
        rng = Range(-1.3, -1.3)
        items = [x for x in rng]
        self.assertTrue(isinstance(items[0], float))
        self.assertEqual(items, [-1.3])

    def test_ascending_step_1(self):
        rng = Range(0,2,1)
        items = [x for x in rng]
        self.assertEqual(items, [0, 1, 2])

    def test_ascending_int_start_float_stop(self):
        rng = Range(-1, .5, 1)
        items = [x for x in rng]
        self.assertEqual(items, [-1, 0])

    def test_float_ascending_int_step(self):
        rng = Range(.5, 2.5, 1)
        items = [x for x in rng]
        self.assertEqual(items, [0.5, 1.5, 2.5])

    def test_int_ascending_float_step(self):
        rng = Range(1, 2, .3)
        items = [x for x in rng]
        self.assertEqual(items, [1, 1.3, 1.6, 1.9])

    def test_descending_float_step(self):
        rng = Range(10, 8.5, -0.5)
        items = [x for x in rng]
        self.assertEqual(items, [10, 9.5, 9.0, 8.5])

    def test_step_opposited_direction(self):
        rng = Range(0, 1, -1)
        items = [x for x in rng]
        self.assertEqual(items, [0])

    # __contains__ tests

    def test_contains_int(self):
        rng = Range(0, 10, 2)
        self.assertTrue(4 in rng)
        self.assertFalse(5 in rng)
        self.assertFalse(-1 in rng)
        self.assertFalse(11 in rng)

    def test_contains_float(self):
        rng = Range(.1, 1.1, .2)
        self.assertTrue(.5 in rng)
        self.assertFalse(.6 in rng)
        self.assertFalse(.05 in rng)
        self.assertFalse(1.2 in rng)

    # __eq__ tests

    def test_equals(self):
        rng1 = Range(0, 10, 2)
        rng2 = Range(0, 10, 2)
        rng3 = Range(0.0, 10.0, 2.0)
        rng4 = Range(0.1, 10, 2.0)
        rng5 = Range(10, 0, -2)
        self.assertTrue(rng1 == rng2)
        self.assertTrue(rng1 == rng3)
        self.assertFalse(rng1 == rng4)
        self.assertFalse(rng1 == rng5)
        
    # __repr__ tests

    def test_int_repr(self):
        rng = Range(0, 10, 2)
        self.assertEqual(repr(rng), 'Range("0-10:2")')

    def test_float_repr(self):
        rng = Range(0.1, 1., 2.)
        self.assertEqual(repr(rng), 'Range("0.1-1.0:2.0")')

    def test_mixed_repr(self):
        rng = Range(0.1, 10, 2.)
        self.assertEqual(repr(rng), 'Range("0.1-10:2.0")')

    # __str__ tests

    def test_single_int_str(self):
        rng = Range(1)
        self.assertEqual(str(rng), "1")

    def test_default_step_str(self):
        rng = Range(1, 10)
        self.assertEqual(str(rng), "1-10")

    def test_int_str(self):
        rng = Range(0, 10, 2)
        self.assertEqual(str(rng), "0-10:2")

    def test_float_str(self):
        rng = Range(0.1, 1., 2.)
        self.assertEqual(str(rng), "0.1-1.0:2.0")

    def test_mixed_str(self):
        rng = Range(0.1, 10, 2.)
        self.assertEqual(str(rng), "0.1-10:2.0")
    
    # enumerate tests

    def test_enumerate_int(self):
        rng = Range(0, 4, 2)
        items = [i for i in rng.enumerate()]
        self.assertEqual(items, [(0, 0), (1, 2), (2, 4)])

    def test_enumerate_float(self):
        rng = Range(0, .4, .2)
        items = [i for i in rng.enumerate()]
        self.assertEqual(items, [(0, 0), (1, .2), (2, .4)])

    def test_enumerate_start(self):
        rng = Range(0, 4, 2)
        items = [i for i in rng.enumerate(start=3)]
        self.assertEqual(items, [(3, 0), (4, 2), (5, 4)])

    # first_middle_last tests

    def test_single_int_range(self):
        rng = Range(42)
        self.assertEqual(rng.first_middle_last(), (42, 42, 42))

    def test_int_range(self):
        rng = Range(0, 4, 2)
        self.assertEqual(rng.first_middle_last(), (0, 2, 4))

    def test_float_range(self):
        rng = Range(0, .4, .2)
        self.assertEqual(rng.first_middle_last(), (0, .2, .4))

    def test_int_range_even_number_of_items(self):
        rng = Range(0, 10, 2)
        self.assertEqual(rng.first_middle_last(), (0, 4, 10))

    # reverse tests

    def test_int_asc_to_desc(self):
        rng = Range(0, 10, 2, repeat=3)
        rng.reverse()
        self.assertEqual(rng.start, 10)
        self.assertEqual(rng.stop, 0)
        self.assertEqual(rng.step, -2)
        self.assertEqual(rng.repeat, 3)

    def test_int_desc_to_asc(self):
        rng = Range(10, 0, -2, repeat=3)
        rng.reverse()
        self.assertEqual(rng.start, 0)
        self.assertEqual(rng.stop, 10)
        self.assertEqual(rng.step, 2)
        self.assertEqual(rng.repeat, 3)

    def test_float_asc_to_desc(self):
        rng = Range(0, 1.0, .2, repeat=3)
        rng.reverse()
        self.assertEqual(rng.start, 1.0)
        self.assertEqual(rng.stop, 0)
        self.assertEqual(rng.step, -.2)
        self.assertEqual(rng.repeat, 3)

    def test_float_desc_to_asc(self):
        rng = Range(1.0, 0, -.2, repeat=3)
        rng.reverse()
        self.assertEqual(rng.start, 0)
        self.assertEqual(rng.stop, 1.0)
        self.assertEqual(rng.step, .2)
        self.assertEqual(rng.repeat, 3)

    # property getter tests

    def test_int_range_properties_get(self):
        rng = Range(0, 10, 2, repeat=3)
        self.assertTrue(isinstance(rng.start, int))
        self.assertEqual(rng.start, 0)
        self.assertTrue(isinstance(rng.stop, int))
        self.assertEqual(rng.stop, 10)
        self.assertTrue(isinstance(rng.step, int))
        self.assertEqual(rng.step, 2)
        self.assertTrue(isinstance(rng.repeat, int))
        self.assertEqual(rng.repeat, 3)

    def test_float_range_properties_get(self):
        rng = Range(0.1, 1.0, .2, repeat=3)
        self.assertTrue(isinstance(rng.start, float))
        self.assertEqual(rng.start, 0.1)
        self.assertTrue(isinstance(rng.stop, float))
        self.assertEqual(rng.stop, 1.0)
        self.assertTrue(isinstance(rng.step, float))
        self.assertEqual(rng.step, .2)
        self.assertTrue(isinstance(rng.repeat, int))
        self.assertEqual(rng.repeat, 3)

    # property setter tests

    def test_int_range_property_set(self):
        rng = Range(0, 10, 2, repeat=3)
        rng.start = 1
        rng.stop = 11
        rng.step = 3
        rng.repeat = 2
        self.assertEqual(rng.start, 1)
        self.assertEqual(rng.stop, 11)
        self.assertEqual(rng.step, 3)
        self.assertEqual(rng.repeat, 2)
        self.assertRaises(ValueError, lambda: setattr(rng, 'repeat', 'a'))
        self.assertRaises(ValueError, lambda: setattr(rng, 'repeat', '0'))
        self.assertRaises(ValueError, lambda: setattr(rng, 'repeat', '-1'))
        self.assertRaises(ValueError, lambda: setattr(rng, 'repeat', '.1'))

    def test_float_range_property_set(self):
        rng = Range(0.1, 1.0, .2, repeat=3)
        rng.start = .2
        rng.stop = 1.1
        rng.step = .3
        rng.repeat = 2
        self.assertEqual(rng.start, .2)
        self.assertEqual(rng.stop, 1.1)
        self.assertEqual(rng.step, .3)
        self.assertEqual(rng.repeat, 2)

    # __getitem__ tests

    def test_int_range_indexing(self):
        rng = Range(1, 10, 2)
        self.assertEqual(rng[0], 1)
        self.assertEqual(rng[1], 3)
        self.assertEqual(rng[2], 5)
        self.assertEqual(rng[3], 7)
        self.assertEqual(rng[4], 9)

    def test_int_range_indexing_with_repeat(self):
        rng = Range(1, 10, 2, repeat=2)
        self.assertEqual(rng[0], 1)
        self.assertEqual(rng[1], 3)
        self.assertEqual(rng[2], 5)
        self.assertEqual(rng[3], 7)
        self.assertEqual(rng[4], 9)
        self.assertEqual(rng[5], 1)
        self.assertEqual(rng[6], 3)
        self.assertEqual(rng[7], 5)
        self.assertEqual(rng[8], 7)
        self.assertEqual(rng[9], 9)

    def test_float_range_indexing(self):
        rng = Range(.1, 1.0, .2)
        self.assertEqual(rng[0], .1)
        self.assertEqual(rng[1], .3)
        self.assertEqual(rng[2], .5)
        self.assertEqual(rng[3], .7)
        self.assertEqual(rng[4], .9)

    def test_float_range_indexing_with_repeat(self):
        rng = Range(.1, 1.0, .2, repeat=2)
        self.assertEqual(rng[0], .1)
        self.assertEqual(rng[1], .3)
        self.assertEqual(rng[2], .5)
        self.assertEqual(rng[3], .7)
        self.assertEqual(rng[4], .9)
        self.assertEqual(rng[5], .1)
        self.assertEqual(rng[6], .3)
        self.assertEqual(rng[7], .5)
        self.assertEqual(rng[8], .7)
        self.assertEqual(rng[9], .9)

    # __len__ tests

    def test_len_single(self):
        rng = Range(0, 10, 2)
        self.assertEqual(len(rng), 6)

    def test_len_repeat(self):
        rng = Range(0, 10, 2, repeat=2)
        self.assertEqual(len(rng), 12)

    # index tests

    def test_index_int(self):
        rng = Range(0, 10, 2)
        self.assertEqual(rng.index(4), 2)

    def test_index_float(self):
        rng = Range(0, 1.0, .2)
        self.assertEqual(rng.index(.4), 2)

    def test_not_in_range(self):
        rng = Range(0, 10, 2)
        self.assertRaises(ValueError, rng.index, 1)
        self.assertRaises(ValueError, rng.index, -1)
        self.assertRaises(ValueError, rng.index, 11)

    # count tests

    def test_count_simple(self):
        rng = Range(0, 10, 2)
        self.assertEqual(rng.count(4), 1)

    def test_count_repeat(self):
        rng = Range(0, 10, 2, repeat=4)
        self.assertEqual(rng.count(4), 4)


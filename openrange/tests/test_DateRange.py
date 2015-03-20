from datetime import date, timedelta
import unittest

from openrange.dt import DateRange

class TestDateRange(unittest.TestCase):

    def setUp(self):
        self.date1 = date(2015, 3, 1)
        self.date2 = date(2015, 3, 31) 
        self.delta = timedelta(days=7)

    def test_bad_args(self):

        args1 = ("foo", self.date2, self.delta)
        self.assertRaises(TypeError, DateRange, *args1)

        args2 = (self.date1, "foo", self.delta)
        self.assertRaises(TypeError, DateRange, *args2)

        args3 = (self.date1, self.date2, "foo")
        self.assertRaises(TypeError, DateRange, *args3)

    def test_iter(self):
        
        dr = DateRange(self.date1, self.date2, self.delta)
        dates = [d for d in dr]
        self.assertEqual(dates, [
            date(2015, 3, 1),
            date(2015, 3, 8),
            date(2015, 3, 15),
            date(2015, 3, 22),
            date(2015, 3, 29)
        ])

    def test_iter_neg_step(self):

        dr = DateRange(self.date2, self.date1, -1 * self.delta)
        dates = [d for d in dr]
        self.assertEqual(dates, [
            date(2015, 3, 31),
            date(2015, 3, 24),
            date(2015, 3, 17),
            date(2015, 3, 10),
            date(2015, 3, 3)
        ])

    def test_contains(self):

        dr = DateRange(self.date1, self.date2, self.delta)
        self.assertEquals(date(2015, 3, 15) in dr, True)

    def test_equals(self):
        
        dr1 = DateRange(self.date1, self.date2, self.delta)
        dr2 = DateRange(self.date1, self.date2, self.delta)
        self.assertEquals(dr1, dr2)

    def test_enumerate(self):
        
        dr = DateRange(self.date1, self.date2, self.delta)
        dates = [d for d in dr.enumerate()]
        self.assertEqual(dates, [
            (0, date(2015, 3, 1)),
            (1, date(2015, 3, 8)),
            (2, date(2015, 3, 15)),
            (3, date(2015, 3, 22)),
            (4, date(2015, 3, 29))
        ])

    def test_excluding(self):

        dr = DateRange(self.date1, self.date2, self.delta)
        excludes = [date(2015, 3, 8), date(2015, 3, 22)]
        dates = [d for d in dr.excluding(excludes)]
        self.assertEqual(dates, [
            date(2015, 3, 1),
            date(2015, 3, 15),
            date(2015, 3, 29)
        ])

    def test_reverse(self):

        dr = DateRange(self.date1, self.date2, self.delta)
        dr.reverse()
        dates = [d for d in dr]
        self.assertEqual(dates, [
            date(2015, 3, 31),
            date(2015, 3, 24),
            date(2015, 3, 17),
            date(2015, 3, 10),
            date(2015, 3, 3)
        ])
    
    def test_properties_get(self):
        
        dr = DateRange(self.date1, self.date2, self.delta)
        self.assertEqual(dr.start, self.date1)
        self.assertEqual(dr.stop, self.date2)
        self.assertEqual(dr.step, self.delta)

    def test_indexing(self):
    
        dr = DateRange(self.date1, self.date2, self.delta)
        self.assertEqual(dr[0], date(2015, 3, 1))
        self.assertEqual(dr[1], date(2015, 3, 8))
        self.assertEqual(dr[2], date(2015, 3, 15))
        self.assertEqual(dr[3], date(2015, 3, 22))
        self.assertEqual(dr[4], date(2015, 3, 29))

    def test_len(self):

        dr = DateRange(self.date1, self.date2, self.delta)
        self.assertEqual(len(dr), 5)

    def test_index(self):

        dr = DateRange(self.date1, self.date2, self.delta)
        self.assertEqual(dr.index(date(2015, 3, 15)), 2)
    
    def test_count(self):
        
        dr = DateRange(self.date1, self.date2, self.delta)
        self.assertEqual(dr.count(date(2015, 3, 15)), 1)


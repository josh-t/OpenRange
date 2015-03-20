from datetime import datetime, timedelta
import unittest

from openrange.dt import DatetimeRange

class TestDatetimeRange(unittest.TestCase):

    def setUp(self):
        self.dt1 = datetime(2015, 3, 1, 16, 30)
        self.dt2 = datetime(2015, 3, 4, 7, 15) 
        self.delta = timedelta(hours=12)

    def test_bad_args(self):

        args1 = ("foo", self.dt2, self.delta)
        self.assertRaises(TypeError, DatetimeRange, *args1)

        args2 = (self.dt1, "foo", self.delta)
        self.assertRaises(TypeError, DatetimeRange, *args2)

        args3 = (self.dt1, self.dt2, "foo")
        self.assertRaises(TypeError, DatetimeRange, *args3)

    def test_iter(self):
        
        dtr = DatetimeRange(self.dt1, self.dt2, self.delta)
        dates = [d for d in dtr]
        self.assertEqual(dates, [
            datetime(2015, 3, 1, 16, 30),
            datetime(2015, 3, 2, 4, 30),
            datetime(2015, 3, 2, 16, 30),
            datetime(2015, 3, 3, 4, 30),
            datetime(2015, 3, 3, 16, 30),
            datetime(2015, 3, 4, 4, 30)
        ])

    def test_iter_neg_step(self):

        dtr = DatetimeRange(self.dt2, self.dt1, -1 * self.delta)
        dates = [d for d in dtr]
        self.assertEqual(dates, [
            datetime(2015, 3, 4, 7, 15),
            datetime(2015, 3, 3, 19, 15),
            datetime(2015, 3, 3, 7, 15),
            datetime(2015, 3, 2, 19, 15),
            datetime(2015, 3, 2, 7, 15),
            datetime(2015, 3, 1, 19, 15)
        ])

    def test_contains(self):

        dtr = DatetimeRange(self.dt1, self.dt2, self.delta)
        self.assertEquals(datetime(2015, 3, 3, 16, 30) in dtr, True)

    def test_equals(self):
        
        dtr1 = DatetimeRange(self.dt1, self.dt2, self.delta)
        dtr2 = DatetimeRange(self.dt1, self.dt2, self.delta)
        self.assertEquals(dtr1, dtr2)

    def test_enumerate(self):
        
        dtr = DatetimeRange(self.dt1, self.dt2, self.delta)
        dates = [d for d in dtr.enumerate()]
        self.assertEqual(dates, [
            (0, datetime(2015, 3, 1, 16, 30)),
            (1, datetime(2015, 3, 2, 4, 30)),
            (2, datetime(2015, 3, 2, 16, 30)),
            (3, datetime(2015, 3, 3, 4, 30)),
            (4, datetime(2015, 3, 3, 16, 30)),
            (5, datetime(2015, 3, 4, 4, 30))
        ])

    def test_excluding(self):

        dtr = DatetimeRange(self.dt1, self.dt2, self.delta)
        excludes = [
            datetime(2015, 3, 2, 4, 30), 
            datetime(2015, 3, 3, 16, 30)
        ]
        dates = [d for d in dtr.excluding(excludes)]
        self.assertEqual(dates, [
            datetime(2015, 3, 1, 16, 30),
            datetime(2015, 3, 2, 16, 30),
            datetime(2015, 3, 3, 4, 30),
            datetime(2015, 3, 4, 4, 30)
        ])

    def test_reverse(self):

        dtr = DatetimeRange(self.dt1, self.dt2, self.delta)
        dtr.reverse()
        dates = [d for d in dtr]
        self.assertEqual(dates, [
            datetime(2015, 3, 4, 7, 15),
            datetime(2015, 3, 3, 19, 15),
            datetime(2015, 3, 3, 7, 15),
            datetime(2015, 3, 2, 19, 15),
            datetime(2015, 3, 2, 7, 15),
            datetime(2015, 3, 1, 19, 15)
        ])
    
    def test_properties_get(self):
        
        dtr = DatetimeRange(self.dt1, self.dt2, self.delta)
        self.assertEqual(dtr.start, self.dt1)
        self.assertEqual(dtr.stop, self.dt2)
        self.assertEqual(dtr.step, self.delta)

    def test_indexing(self):
    
        dtr = DatetimeRange(self.dt1, self.dt2, self.delta)
        self.assertEqual(dtr[0], datetime(2015, 3, 1, 16, 30))
        self.assertEqual(dtr[1], datetime(2015, 3, 2, 4, 30))
        self.assertEqual(dtr[2], datetime(2015, 3, 2, 16, 30))
        self.assertEqual(dtr[3], datetime(2015, 3, 3, 4, 30))
        self.assertEqual(dtr[4], datetime(2015, 3, 3, 16, 30))
        self.assertEqual(dtr[5], datetime(2015, 3, 4, 4, 30))

    def test_len(self):

        dtr = DatetimeRange(self.dt1, self.dt2, self.delta)
        self.assertEqual(len(dtr), 6)

    def test_index(self):

        dtr = DatetimeRange(self.dt1, self.dt2, self.delta)
        self.assertEqual(dtr.index(datetime(2015, 3, 3, 4, 30)), 3)
    
    def test_count(self):
        
        dtr = DatetimeRange(self.dt1, self.dt2, self.delta)
        self.assertEqual(dtr.count(datetime(2015, 3, 4, 4, 30)), 1)


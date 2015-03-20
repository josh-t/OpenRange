from datetime import time, timedelta
import unittest

from openrange.dt import TimeRange

class TestTimeRange(unittest.TestCase):

    def setUp(self):
        self.time1 = time(1, 30)
        self.time2 = time(23, 45)
        self.delta = timedelta(hours=4.5)

    def test_bad_args(self):

        args1 = ("foo", self.time2, self.delta)
        self.assertRaises(TypeError, TimeRange, *args1)

        args2 = (self.time1, "foo", self.delta)
        self.assertRaises(TypeError, TimeRange, *args2)

        args3 = (self.time1, self.time2, "foo")
        self.assertRaises(TypeError, TimeRange, *args3)

    def test_iter(self):
        
        tr = TimeRange(self.time1, self.time2, self.delta)
        times = [t for t in tr]
        self.assertEqual(times, [
            time(1, 30), 
            time(6, 0),
            time(10, 30),
            time(15, 0),
            time(19, 30)
        ])

    def test_iter_neg_step(self):

        tr = TimeRange(self.time2, self.time1, -1 * self.delta)
        times = [t for t in tr]
        self.assertEqual(times, [
            time(23, 45),
            time(19, 15),
            time(14, 45),
            time(10, 15),
            time(5, 45),
        ])

    def test_contains(self):

        tr = TimeRange(self.time1, self.time2, self.delta)
        self.assertEquals(time(15, 0) in tr, True)

    def test_equals(self):
        
        tr1 = TimeRange(self.time1, self.time2, self.delta)
        tr2 = TimeRange(self.time1, self.time2, self.delta)
        self.assertEquals(tr1, tr2)

    def test_enumerate(self):
        
        tr = TimeRange(self.time1, self.time2, self.delta)
        times = [t for t in tr.enumerate()]
        self.assertEqual(times, [
            (0, time(1, 30)),
            (1, time(6, 0)),
            (2, time(10, 30)),
            (3, time(15, 0)),
            (4, time(19, 30))
        ])

    def test_excluding(self):

        tr = TimeRange(self.time1, self.time2, self.delta)
        excludes = [time(6, 0), time(15, 0)]
        times = [t for t in tr.excluding(excludes)]
        self.assertEqual(times, [
            time(1, 30), 
            time(10, 30),
            time(19, 30)
        ])

    def test_reverse(self):

        tr = TimeRange(self.time1, self.time2, self.delta)
        tr.reverse()
        times = [t for t in tr]
        self.assertEqual(times, [
            time(23, 45),
            time(19, 15),
            time(14, 45),
            time(10, 15),
            time(5, 45),
        ])
    
    def test_properties_get(self):
        
        tr = TimeRange(self.time1, self.time2, self.delta)
        self.assertEqual(tr.start, self.time1)
        self.assertEqual(tr.stop, self.time2)
        self.assertEqual(tr.step, self.delta)

    def test_indexing(self):
    
        tr = TimeRange(self.time1, self.time2, self.delta)
        self.assertEqual(tr[0], time(1, 30)) 
        self.assertEqual(tr[1], time(6, 0))
        self.assertEqual(tr[2], time(10, 30))
        self.assertEqual(tr[3], time(15, 0))
        self.assertEqual(tr[4], time(19, 30))

    def test_len(self):

        tr = TimeRange(self.time1, self.time2, self.delta)
        self.assertEqual(len(tr), 5)

    def test_index(self):

        tr = TimeRange(self.time1, self.time2, self.delta)
        self.assertEqual(tr.index(time(10, 30)), 2)
    
    def test_count(self):
        
        tr = TimeRange(self.time1, self.time2, self.delta)
        self.assertEqual(tr.count(time(15, 0)), 1)


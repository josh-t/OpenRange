import unittest
from openrange import BaseRange

class TestBaseRange(unittest.TestCase):

    def test_no_construct(self):
        self.assertRaises(TypeError, BaseRange, None)


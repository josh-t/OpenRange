import unittest
from openrange import BaseRange

class TestBaseRange(unittest.TestCase):

    def setUp(self):
        pass

    # __init__ tests

    def test_no_construct(self):
        self.assertRaises(TypeError, BaseRange, None)


import unittest

import pandas as pd

from reamber.base import Hold


class TestHold(unittest.TestCase):
    """ The purpose of this test is to test the architecture of Base. """

    def setUp(self) -> None:
        self.hold = Hold(offset=1000, column=1, length=1000)

    # @profile
    def test_type(self):
        self.assertTrue(isinstance(self.hold.data, pd.Series))

    def test_eq(self):
        self.assertEqual(Hold(offset=1000, column=1, length=1000), self.hold)
        self.assertNotEqual(Hold(offset=1000, column=1, length=2000), self.hold)

    def test_length(self):
        self.assertEqual(1000, self.hold.length)

    def test_tail_offset(self):
        self.assertEqual(2000, self.hold.tail_offset)

    def test_deepcopy(self):
        self.assertFalse(self.hold is Hold(offset=1000, column=1, length=1000))
        self.assertFalse(self.hold is self.hold.deepcopy())
        hold = self.hold
        self.assertTrue(self.hold is hold)

    def test_length_op(self):
        self.assertEqual(1000, self.hold.length)
        self.hold.length *= 2
        self.assertEqual(2000, self.hold.length)
        self.assertEqual(3000, self.hold.tail_offset)
        # An odd occurrence, but we support negative lengths.
        self.hold.length = -1000
        self.assertEqual(-1000, self.hold.length)
        self.assertEqual(0, self.hold.tail_offset)


if __name__ == '__main__':
    unittest.main()

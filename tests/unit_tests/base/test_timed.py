import unittest

import pandas as pd

from reamber.base import Timed
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *


class TestTimed(unittest.TestCase):
    """ The purpose of this test is to test the architecture of Base. """

    def setUp(self) -> None:
        self.timed = Timed(offset=1000)

    # @profile
    def test_offset(self):
        self.assertEqual(1000, self.timed.offset)

    def test_type(self):
        self.assertTrue(isinstance(self.timed.data, pd.Series))

    def test_eq(self):
        self.assertEqual(Timed(offset=1000), self.timed)

    def test_op_gt(self):
        self.assertTrue(self.timed < Timed(offset=2000))

    def test_op_lt(self):
        self.assertTrue(self.timed > Timed(offset=500))

    def test_deepcopy(self):
        self.assertFalse(self.timed is Timed(offset=1000))
        self.assertFalse(self.timed is self.timed.deepcopy())
        timed = self.timed
        self.assertTrue(self.timed is timed)

    def test_offset_op(self):
        timed = Timed(offset=500)
        self.assertEqual(500, timed.offset)
        timed.offset *= 2
        self.assertEqual(1000, timed.offset)
        _ = timed.offset * 2
        self.assertEqual(1000, timed.offset)

    def test_sort(self):
        objs = [Timed(i) for i in reversed(range(10))]  # [9 -> 0]
        objs.sort()
        self.assertEqual([Timed(i) for i in range(10)], objs)

    def test_from_series(self):
        """ From series is an alternative to initializing the class via the base representation.

        For example, Timed.from_series(data=pd.Series) will call the __init__ via its dict decomposition. """

        timed = Timed.from_series(pd.Series(dict(offset=1000)))
        self.assertEqual(self.timed, timed)

    def test_from_series_excess_args(self):
        """ Ideally, if we have excess arguments, it should be able to remove those"""

        timed = Timed.from_series(pd.Series(dict(offset=1000, a=2000)))
        self.assertEqual(self.timed, timed)

    def test_from_series_missing_args(self):
        """ If there are missing args, it should fail """

        with self.assertRaises(TypeError):
            _ = Timed.from_series(pd.Series(dict(a=2000)))

    def test_from_series_no_args(self):
        """ If there are no args, it should fail """

        with self.assertRaises(TypeError):
            _ = Timed.from_series(pd.Series(dict(), dtype=object))


if __name__ == '__main__':
    unittest.main()

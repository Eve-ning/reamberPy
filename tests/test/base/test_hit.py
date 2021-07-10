import unittest

import pandas as pd

from reamber.base import Hit


class TestHit(unittest.TestCase):
    """ Not much to test here since Hit is basically Note. """

    def setUp(self) -> None:
        self.hit = Hit(offset=1000, column=1)

    # @profile
    def test_type(self):
        self.assertTrue(isinstance(self.hit.data, pd.Series))

    def test_from_series(self):
        hit = Hit.from_series(pd.Series(dict(offset=1000, column=1)))
        self.assertEqual(self.hit, hit)


if __name__ == '__main__':
    unittest.main()

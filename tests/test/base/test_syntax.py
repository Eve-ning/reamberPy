import unittest

from reamber.base import Timed
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *


class TestSyntax(unittest.TestCase):
    """ The purpose of this test is to test the architecture of Base. """

    def setUp(self) -> None:
        self.timed = Timed(offset=1000)

    # # @profile
    # def test_timed(self):
    #     self.assertEqual(1001, self.timed.offset)
    #

if __name__ == '__main__':
    unittest.main()

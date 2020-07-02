import unittest
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *


class TestBpmBeatOffsets(unittest.TestCase):

    # @profile
    def test_osu(self):
        m = OsuMap()
        m.readFile(OSU_CARAVAN)
        m.bpms.snapOffsets(nths=4, lastOffset=10000)


if __name__ == '__main__':
    unittest.main()

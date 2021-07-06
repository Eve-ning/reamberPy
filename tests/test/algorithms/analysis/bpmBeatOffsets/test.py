import unittest
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *


class TestBpmBeatOffsets(unittest.TestCase):

    # @profile
    def test_osu(self):
        m = OsuMap.readFile(OSU_CARAVAN)
        m.bpms.snap_offsets(nths=4, last_offset=10000)


if __name__ == '__main__':
    unittest.main()

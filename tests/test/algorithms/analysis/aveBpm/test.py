import unittest

from reamber.algorithms.analysis.bpm.aveBpm import aveBpm
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *


class TestBpmBeatOffsets(unittest.TestCase):

    def test_osu(self):
        m = OsuMap()
        m.readFile(OSU_CARAVAN)

        aveBpm(m)


if __name__ == '__main__':
    unittest.main()

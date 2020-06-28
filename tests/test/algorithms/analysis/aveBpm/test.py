import unittest
from tests.test.RSC_PATHS import *

from reamber.algorithms.analysis.bpm.aveBpm import aveBpm
from reamber.osu.OsuMapObj import OsuMapObj

class TestBpmBeatOffsets(unittest.TestCase):

    def test_osu(self):
        m = OsuMapObj()
        m.readFile(OSU_CARAVAN)

        ave = aveBpm(m)


if __name__ == '__main__':
    unittest.main()

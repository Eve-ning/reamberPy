import unittest
from tests.test.RSC_PATHS import *

from reamber.osu.OsuMapObj import OsuMapObj
from reamber.algorithms.analysis.bpm.bpmBeatOffsets import bpmBeatOffsets

class TestBpmBeatOffsets(unittest.TestCase):

    # @profile
    def test_osu(self):
        m = OsuMapObj()
        m.readFile("../../../../../" + OSU_CARAVAN)
        print(bpmBeatOffsets(m.bpms, 4, 10000))


if __name__ == '__main__':
    unittest.main()

import unittest

from reamber.algorithms.analysis.bpm.bpmBeatOffsets import bpmBeatOffsets
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *


class TestBpmBeatOffsets(unittest.TestCase):

    # @profile
    def test_osu(self):
        m = OsuMap()
        m.readFile(OSU_CARAVAN)
        bpmBeatOffsets(m.bpms, 4, 10000)


if __name__ == '__main__':
    unittest.main()

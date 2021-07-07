import unittest

from reamber.algorithms.generate.sv.SvSequence import SvSequence
from reamber.osu.OsuMap import OsuMap
from reamber.osu.OsuSv import OsuSv
from tests.test.RSC_PATHS import *


class TestIO(unittest.TestCase):

    def testSv(self):
        # Complex BPM Points
        osu = OsuMap.read_file(OSU_CARAVAN)

        seq = SvSequence()
        seq.read_sv_from_map(osu)

        for sv, sv0 in zip(seq.write_as_sv(OsuSv, volume=0)[:50], osu.svs):
            assert isinstance(sv, OsuSv)
            self.assertAlmostEqual(sv0.multiplier, sv.multiplier)
            self.assertEqual(0, sv.volume)

    def testTrueSv(self):
        # Complex BPM Points
        osu = OsuMap.read_file(OSU_CARAVAN)

        seq = SvSequence()
        seq.read_true_sv_from_map(osu, 140)

        # Just need to check the first 50, others should be ok.
        for sv in seq.write_as_sv(OsuSv, volume=0)[:50]:
            assert isinstance(sv, OsuSv)
            self.assertAlmostEqual(1, sv.multiplier, delta=0.01)
            self.assertEqual(0, sv.volume)


if __name__ == '__main__':
    unittest.main()

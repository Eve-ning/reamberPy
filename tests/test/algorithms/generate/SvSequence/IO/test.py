import unittest
from reamber.algorithms.generate.sv.SvSequence import SvSequence
from reamber.osu.OsuSvObj import OsuSvObj
from reamber.osu.OsuMapObj import OsuMapObj
from tests.test.RSC_PATHS import *

class TestIO(unittest.TestCase):

    def testSv(self):
        # Complex BPM Points
        osu = OsuMapObj()
        osu.readFile(OSU_CARAVAN)

        seq = SvSequence()
        seq.readSvFromMap(osu)

        for sv, sv0 in zip(seq.writeAsSv(OsuSvObj, volume=0)[:50], osu.svs):
            assert isinstance(sv, OsuSvObj)
            self.assertAlmostEqual(sv0.multiplier, sv.multiplier)
            self.assertEqual(0, sv.volume)

    def testTrueSv(self):
        # Complex BPM Points
        osu = OsuMapObj()
        osu.readFile(OSU_CARAVAN)

        seq = SvSequence()
        seq.readTrueSvFromMap(osu, 140)

        # Just need to check the first 50, others should be ok.
        for sv in seq.writeAsSv(OsuSvObj, volume=0)[:50]:
            assert isinstance(sv, OsuSvObj)
            self.assertAlmostEqual(1, sv.multiplier, delta=0.01)
            self.assertEqual(0, sv.volume)


if __name__ == '__main__':
    unittest.main()

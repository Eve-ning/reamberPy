import unittest

from reamber.osu.OsuMap import OsuMap
from reamber.quaver.QuaMap import QuaMap
from reamber.sm.SMMapSet import SMMapSet
from tests.test.RSC_PATHS import *


class TestMutateRate(unittest.TestCase):
    def test_osu(self):
        m = OsuMap.readFile(OSU_PLANET_SHAPER)
        offset = m.notes.offsets(flatten=True)[:10]
        m.rate(2.0, inplace=True)
        for i, j in zip(offset, m.notes.offsets(flatten=True)[:10]):
            self.assertAlmostEqual(i / 2, j)

    def test_qua(self):
        m = QuaMap.readFile(QUA_NEURO_CLOUD)
        offset = m.notes.offsets(flatten=True)[:10]
        m.rate(2.0, inplace=True)
        for i, j in zip(offset, m.notes.offsets(flatten=True)[:10]):
            self.assertAlmostEqual(i / 2, j)

    def test_sm(self):
        s = SMMapSet.readFile(SM_CARAVAN)
        offset = s.maps[0].notes.offsets(flatten=True)[:10]
        s.rate(2.0, inplace=True)
        for i, j in zip(offset, s.maps[0].notes.offsets(flatten=True)[:10]):
            self.assertAlmostEqual(i / 2, j)

if __name__ == '__main__':
    unittest.main()

import unittest

from reamber.algorithms.mutate.rate import rate
from reamber.osu.OsuMap import OsuMap
from reamber.quaver.QuaMap import QuaMap
from reamber.sm.SMMapSet import SMMapSet
from tests.test.RSC_PATHS import *


class TestMutateRate(unittest.TestCase):
    def test_osu(self):
        m = OsuMap()
        m.readFile(OSU_PLANET_SHAPER)
        rate(m, 2.0, inplace=True)
        m.writeFile("out.osu")

    def test_qua(self):
        m = QuaMap()
        m.readFile(QUA_NEURO_CLOUD)
        rate(m, 2.0, inplace=True)
        m.writeFile("out.qua")

    def test_sm(self):
        s = SMMapSet()
        s.readFile(SM_CARAVAN)
        rate(s, 2.0, inplace=True)
        s.writeFile("out.sm")


if __name__ == '__main__':
    unittest.main()

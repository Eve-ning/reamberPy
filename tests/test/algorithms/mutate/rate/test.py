import unittest
from tests.test.RSC_PATHS import *

from reamber.osu.OsuMapObj import OsuMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from reamber.sm.SMMapSetObj import SMMapSetObj

from reamber.algorithms.mutate.rate import rate
import os

class TestMutateRate(unittest.TestCase):
    def test_osu(self):
        m = OsuMapObj()
        m.readFile(OSU_PLANET_SHAPER)
        rate(m, 2.0, inplace=True)
        m.writeFile("out.osu")

    def test_qua(self):
        m = QuaMapObj()
        m.readFile(QUA_NEURO_CLOUD)
        rate(m, 2.0, inplace=True)
        m.writeFile("out.qua")

    def test_sm(self):
        s = SMMapSetObj()
        s.readFile(SM_CARAVAN)
        rate(s, 2.0, inplace=True)
        s.writeFile("out.sm")


if __name__ == '__main__':
    unittest.main()

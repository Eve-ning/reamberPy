import unittest
from tests.test.RSC_PATHS import *

from reamber.osu.OsuMapObj import OsuMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from reamber.sm.SMMapSetObj import SMMapSetObj

from reamber.algorithms.mutate.mutateRate import mutateRate


class TestMutateRate(unittest.TestCase):
    def test_osu(self):
        m = OsuMapObj()
        m.readFile("../../../../../" + OSU_PLANET_SHAPER)
        mutateRate(m, 2.0, inplace=True)
        m.writeFile("planetshaper.osu")

    def test_qua(self):
        m = QuaMapObj()
        m.readFile("../../../../../" + QUA_NEURO_CLOUD)
        mutateRate(m, 2.0, inplace=True)
        m.writeFile("neurocloud.qua")

    def test_sm(self):
        s = SMMapSetObj()
        s.readFile("../../../../../" + SM_CARAVAN)
        mutateRate(s, 2.0, inplace=True)
        s.writeFile("caravan.sm")


if __name__ == '__main__':
    unittest.main()

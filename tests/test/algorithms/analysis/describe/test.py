import unittest

from reamber.algorithms.analysis.describe.describe import describe
from reamber.o2jam.O2JMapSet import O2JMapSet
from reamber.osu.OsuMap import OsuMap
from reamber.quaver.QuaMap import QuaMap
from reamber.sm.SMMapSet import SMMapSet
from tests.test.RSC_PATHS import *


class TestDescribe(unittest.TestCase):

    # @profile
    def test_osu(self):
        m = OsuMap()
        m.readFile(OSU_ICFITU)
        describe(m, s=None)

    # @profile
    def test_qua(self):
        m = QuaMap()
        m.readFile(QUA_NEURO_CLOUD)
        describe(m, s=None)

    # @profile
    def test_sm(self):
        s = SMMapSet()
        s.readFile(SM_CARAVAN)
        describe(s.maps[0], s)

    # @profile
    def test_o2j(self):
        s = O2JMapSet()
        s.readFile(O2J_FLY_MAGPIE_OJN)
        describe(s.maps[2], s)


if __name__ == '__main__':
    unittest.main()

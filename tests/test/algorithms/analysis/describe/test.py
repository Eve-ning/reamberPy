import unittest
from tests.test.RSC_PATHS import *
from tests.test.profiling import profile

from reamber.o2jam.O2JMapSetObj import O2JMapSetObj
from reamber.osu.OsuMapObj import OsuMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from reamber.sm.SMMapSetObj import SMMapSetObj
from reamber.algorithms.analysis.describe.describe import describe

class TestDescribe(unittest.TestCase):

    # @profile
    def test_osu(self):
        m = OsuMapObj()
        m.readFile("../../../../../" + OSU_ICFITU)
        describe(m, s=None)

    # @profile
    def test_qua(self):
        m = QuaMapObj()
        m.readFile("../../../../../" + QUA_NEURO_CLOUD)
        describe(m, s=None)

    # @profile
    def test_sm(self):
        s = SMMapSetObj()
        s.readFile("../../../../../" + SM_CARAVAN)
        describe(s.maps[0], s)

    # @profile
    def test_o2j(self):
        s = O2JMapSetObj()
        s.readFile("../../../../../" + O2J_FLY_MAGPIE_OJN)
        describe(s.maps[2], s)

if __name__ == '__main__':
    unittest.main()

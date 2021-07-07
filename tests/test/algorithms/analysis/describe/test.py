import unittest

from reamber.o2jam.O2JMapSet import O2JMapSet
from reamber.osu.OsuMap import OsuMap
from reamber.quaver.QuaMap import QuaMap
from reamber.sm.SMMapSet import SMMapSet
from tests.test.RSC_PATHS import *


class TestDescribe(unittest.TestCase):

    # @profile
    def test_osu(self):
        m = OsuMap.read_file(OSU_ICFITU)
        m.describe()

    # @profile
    def test_qua(self):
        m = QuaMap.read_file(QUA_NEURO_CLOUD)
        m.describe()

    # @profile
    def test_sm(self):
        s = SMMapSet.readFile(SM_CARAVAN)
        s.describe()

    # @profile
    def test_o2j(self):
        s = O2JMapSet.readFile(O2J_FLY_MAGPIE_OJN)
        s.describe()


if __name__ == '__main__':
    unittest.main()

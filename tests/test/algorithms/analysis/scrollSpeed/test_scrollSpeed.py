import unittest

import matplotlib.pyplot as plt
import pandas as pd

from reamber.o2jam.O2JMapSet import O2JMapSet
from reamber.osu.OsuMap import OsuMap
from reamber.quaver.QuaMap import QuaMap
from reamber.sm.SMMapSet import SMMapSet
from tests.test.RSC_PATHS import *


class TestScrollSpeed(unittest.TestCase):

    # @profile
    def test_osu(self):
        m = OsuMap.readFile(OSU_CARAVAN)
        pd.DataFrame(m.scroll_speed()).set_index('offset').plot()
        # plt.savefig("osu.png")

    # @profile
    def test_qua(self):
        m = QuaMap.readFile(QUA_NEURO_CLOUD)
        pd.DataFrame(m.scroll_speed()).set_index('offset').plot()
        # plt.savefig("qua.png")

    # @profile
    def test_sm(self):
        s = SMMapSet.readFile(SM_CARAVAN)
        pd.DataFrame(s.maps[0].scroll_speed()).set_index('offset').plot()
        # plt.savefig("sm.png")

    # @profile
    def test_o2j(self):
        s = O2JMapSet.readFile(O2J_FLY_MAGPIE_OJN)
        pd.DataFrame(s.maps[2].scroll_speed()).set_index('offset').plot()
        # plt.savefig("o2j.png")


if __name__ == '__main__':
    unittest.main()

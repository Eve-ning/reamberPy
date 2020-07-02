import unittest

import matplotlib.pyplot as plt

from reamber.algorithms.plot.nps import npsPlot
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *


class TestNps(unittest.TestCase):

    # @profile
    def test_osu(self):
        m = OsuMap()
        m.readFile(OSU_PLANET_SHAPER)
        plt.style.use('dark_background')
        npsPlot(m, binSize=500)

    # # @profile
    # def test_qua(self):
    #     m = QuaMap()
    #     m.readFile(QUA_NEURO_CLOUD)
    #     plt.style.use('dark_background')
    #     npsPlot(m, "qua.png", binSize=1000)
    #
    # # @profile
    # def test_sm(self):
    #     s = SMMapSet()
    #     s.readFile(SM_CARAVAN)
    #     plt.style.use('dark_background')
    #     npsPlot(s.maps[0], "sm.png")
    #
    # # @profile
    # def test_o2j(self):
    #     s = O2JMapSet()
    #     s.readFile(O2J_FLY_MAGPIE_OJN)
    #     plt.style.use('dark_background')
    #     npsPlot(s.maps[2], "o2j.png")


if __name__ == '__main__':
    unittest.main()

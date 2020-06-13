import unittest
from tests.test.RSC_PATHS import *

from reamber.o2jam.O2JMapSetObj import O2JMapSetObj
from reamber.osu.OsuMapObj import OsuMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from reamber.sm.SMMapSetObj import SMMapSetObj
from reamber.algorithms.analysis.note.nps import npsPlot
import matplotlib.pyplot as plt

class TestNps(unittest.TestCase):

    # @profile
    def test_osu(self):
        m = OsuMapObj()
        m.readFile("../../../../../" + OSU_PLANET_SHAPER)
        plt.style.use('dark_background')
        npsPlot(m, "osu.png", binSize=500)

    # @profile
    def test_qua(self):
        m = QuaMapObj()
        m.readFile("../../../../../" + QUA_NEURO_CLOUD)
        plt.style.use('dark_background')
        npsPlot(m, "qua.png", binSize=1000)

    # @profile
    def test_sm(self):
        s = SMMapSetObj()
        s.readFile("../../../../../" + SM_CARAVAN)
        plt.style.use('dark_background')
        npsPlot(s.maps[0], "sm.png")

    # @profile
    def test_o2j(self):
        s = O2JMapSetObj()
        s.readFile("../../../../../" + O2J_FLY_MAGPIE_OJN)
        plt.style.use('dark_background')
        npsPlot(s.maps[2], "o2j.png")



if __name__ == '__main__':
    unittest.main()

import unittest
from tests.test.RSC_PATHS import *

from reamber.osu.OsuMapObj import OsuMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from reamber.sm.SMMapSetObj import SMMapSetObj
from reamber.o2jam.O2JMapSetObj import O2JMapSetObj
from reamber.algorithms.analysis.bpm.scrollSpeed import scrollSpeed
import matplotlib.pyplot as plt
import pandas as pd

class TestScrollSpeed(unittest.TestCase):

    # @profile
    def test_osu(self):
        m = OsuMapObj()
        m.readFile(OSU_CARAVAN)
        pd.DataFrame(scrollSpeed(m)).set_index('offset').plot()
        plt.savefig("osu.png")

    # @profile
    def test_qua(self):
        m = QuaMapObj()
        m.readFile(QUA_NEURO_CLOUD)
        pd.DataFrame(scrollSpeed(m)).set_index('offset').plot()
        plt.savefig("qua.png")

    # @profile
    def test_sm(self):
        s = SMMapSetObj()
        s.readFile(SM_CARAVAN)
        pd.DataFrame(scrollSpeed(s.maps[0])).set_index('offset').plot()
        plt.savefig("sm.png")

    # @profile
    def test_o2j(self):
        s = O2JMapSetObj()
        s.readFile(O2J_FLY_MAGPIE_OJN)
        pd.DataFrame(scrollSpeed(s.maps[2])).set_index('offset').plot()
        plt.savefig("o2j.png")


if __name__ == '__main__':
    unittest.main()

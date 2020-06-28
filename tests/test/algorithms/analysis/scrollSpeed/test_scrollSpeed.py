import unittest

import matplotlib.pyplot as plt
import pandas as pd

from reamber.algorithms.analysis.bpm.scrollSpeed import scrollSpeed
from reamber.o2jam.O2JMapSet import O2JMapSet
from reamber.osu.OsuMap import OsuMap
from reamber.quaver.QuaMap import QuaMap
from reamber.sm.SMMapSet import SMMapSet
from tests.test.RSC_PATHS import *


class TestScrollSpeed(unittest.TestCase):

    # @profile
    def test_osu(self):
        m = OsuMap()
        m.readFile(OSU_CARAVAN)
        pd.DataFrame(scrollSpeed(m)).set_index('offset').plot()
        plt.savefig("osu.png")

    # @profile
    def test_qua(self):
        m = QuaMap()
        m.readFile(QUA_NEURO_CLOUD)
        pd.DataFrame(scrollSpeed(m)).set_index('offset').plot()
        plt.savefig("qua.png")

    # @profile
    def test_sm(self):
        s = SMMapSet()
        s.readFile(SM_CARAVAN)
        pd.DataFrame(scrollSpeed(s.maps[0])).set_index('offset').plot()
        plt.savefig("sm.png")

    # @profile
    def test_o2j(self):
        s = O2JMapSet()
        s.readFile(O2J_FLY_MAGPIE_OJN)
        pd.DataFrame(scrollSpeed(s.maps[2])).set_index('offset').plot()
        plt.savefig("o2j.png")


if __name__ == '__main__':
    unittest.main()

import unittest

import matplotlib.pyplot as plt

from reamber.algorithms.plot.nps import nps_plot, nps_plot_by_key
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *


class TestNps(unittest.TestCase):

    # @profile
    def test(self):
        plt.clf()
        m = OsuMap.read_file(OSU_PLANET_SHAPER)
        nps_plot(m.notes)
        # plt.savefig('main.png')

    def testByKey(self):
        plt.clf()
        m = OsuMap.read_file(OSU_PLANET_SHAPER)
        nps_plot_by_key(m.notes)
        # plt.savefig('byKey.png')


if __name__ == '__main__':
    unittest.main()

import unittest

import matplotlib.pyplot as plt

from reamber.algorithms.replays import OsuReplayError
from tests.test.RSC_PATHS import *


class TestNps(unittest.TestCase):

    # @profile
    def test(self):
        rep = OsuReplayError([OSU_REP_FINIXE1, OSU_REP_FINIXE2], OSU_FINIXE)
        er = rep.errors()
        # plt.hist([e for k in er.hit_errors[1] for e in k], bins=100)
        # plt.show()


if __name__ == '__main__':
    unittest.main()

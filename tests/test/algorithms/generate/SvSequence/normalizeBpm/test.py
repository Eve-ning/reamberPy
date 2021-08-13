import unittest

from reamber.algorithms.generate.sv.generators.svNormalizeBpm import sv_normalize_bpm
from reamber.base.lists.BpmList import BpmList, Bpm


class TestNormalize(unittest.TestCase):

    def testNormalize(self):
        seq = sv_normalize_bpm(BpmList([Bpm(0, 200), Bpm(100, 50), Bpm(300, 100)]), 100)
        self.assertAlmostEqual(seq[0].multiplier, 0.5)
        self.assertAlmostEqual(seq[1].multiplier, 2.0)
        self.assertAlmostEqual(seq[2].multiplier, 1.0)


if __name__ == '__main__':
    unittest.main()

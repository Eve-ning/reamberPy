import unittest

from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence, SvObj


class TestCross(unittest.TestCase):

    def test(self):
        # Test Cross
        seq = SvSequence([SvObj(0, 0.5), SvObj(100, 2.0), SvObj(200, 3.0), SvObj(400, 2.0)])
        seq2 = SvSequence([SvObj(50, 0.1), SvObj(100, 10.0), SvObj(250, 5.0), SvObj(500, 0.3)])
        seq.crossWith(seq2, inplace=True)

        self.assertAlmostEqual(seq[0].multiplier, 0.5)
        self.assertAlmostEqual(seq[1].multiplier, 20.0)
        self.assertAlmostEqual(seq[2].multiplier, 30.0)
        self.assertAlmostEqual(seq[3].multiplier, 10.0)

    def test2(self):
        # Test Mutual Cross
        seq1 = SvSequence([SvObj(0, 0.5), SvObj(100, 2.0), SvObj(200, 3.0), SvObj(400, 2.0)])
        seq2 = SvSequence([SvObj(50, 0.1), SvObj(100, 10.0), SvObj(250, 5.0), SvObj(500, 0.2)])
        seq = SvPkg.crossMutualWith(seq1, seq2).combine(SvPkg.CombineMethod.DROP_BY_POINT)

        self.assertAlmostEqual(seq[0].multiplier, 0.5)
        self.assertAlmostEqual(seq[1].multiplier, 0.05)
        self.assertAlmostEqual(seq[2].multiplier, 20.0)
        self.assertAlmostEqual(seq[3].multiplier, 30.0)
        self.assertAlmostEqual(seq[4].multiplier, 15.0)
        self.assertAlmostEqual(seq[5].multiplier, 10.0)
        self.assertAlmostEqual(seq[6].multiplier, 0.4)


if __name__ == '__main__':
    unittest.main()

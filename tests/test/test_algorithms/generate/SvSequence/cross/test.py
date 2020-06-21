import unittest
from reamber.algorithms.generate.sv.SvSequence import SvSequence,SvObj
from reamber.algorithms.generate.sv.SvPkg import SvPkg


class TestSvSequence(unittest.TestCase):

    def test4(self):
        # Test Cross
        seq = SvSequence([SvObj(0, 0.5), SvObj(100, 2.0), SvObj(200, 3.0), SvObj(400, 2.0)])
        seq2 = SvSequence([SvObj(50, 0.1), SvObj(101, 10.0)])
        seq.crossWith(seq2)
        print(seq)

    def test5(self):
        # Test Mutual Cross
        seq = SvSequence([(0, 0.5), (100, 2.0), (200, 3.0), (400, 2.0)])
        seq2 = SvSequence([(50, 0.1), (101, 10.0)])
        print(SvPkg.crossMutualWith(seq, seq2).combine())





if __name__ == '__main__':
    unittest.main()

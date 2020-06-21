import unittest
from reamber.algorithms.generate.sv.SvSequence import SvSequence,SvObj
from reamber.algorithms.generate.sv.SvPkg import SvPkg


class TestFit(unittest.TestCase):

    def testFit(self):
        # Test Fitting
        seq = SvSequence([SvObj(0, 0.5), SvObj(50, 1.5), SvObj(100, 1.0)])
        print(SvPkg.fit(seq, [0, 100, 200, 400, 600]).combine(SvPkg.CombineMethod.DROP_BY_POINT))





if __name__ == '__main__':
    unittest.main()

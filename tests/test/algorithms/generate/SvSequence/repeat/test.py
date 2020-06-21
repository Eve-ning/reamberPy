import unittest
from reamber.algorithms.generate.sv.SvSequence import SvSequence,SvObj
from reamber.algorithms.generate.sv.SvPkg import SvPkg


class TestRepeat(unittest.TestCase):

    def testRepeat(self):
        # Test Repeat
        seq = SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)])
        print(SvPkg.repeat(seq, 3).combine(SvPkg.CombineMethod.DROP_BY_POINT))



if __name__ == '__main__':
    unittest.main()

import unittest
from reamber.algorithms.generate.sv.SvSequence import SvSequence,SvObj
from reamber.algorithms.generate.sv.SvPkg import SvPkg


class TestSvSequence(unittest.TestCase):
 
    def testCopy(self):
        # Test Copy
        seq = SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)])
        print(SvPkg.copyTo(seq=seq,offsets=[100, 200, 300])
              .combine(combineMethod=SvPkg.CombineMethod.DROP_BY_POINT))

    def testRepeat(self):
        # Test Repeat
        seq = SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)])
        print(SvPkg.repeat(seq, 3).combine(SvPkg.CombineMethod.DROP_BY_POINT))





if __name__ == '__main__':
    unittest.main()

import unittest

from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence, SvObj


class TestCopyTo(unittest.TestCase):
 
    def testCopy(self):
        # Test Copy
        seq = SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)])
        seqCopy = SvPkg.copy_to(seq=seq, offsets=[100, 200, 300]).combine(
            combine_method=SvPkg.CombineMethod.DROP_BY_POINT)
        self.assertEqual(len(seqCopy), 4)


if __name__ == '__main__':
    unittest.main()

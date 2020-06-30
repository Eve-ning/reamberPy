import unittest

from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence, SvObj


class TestRepeat(unittest.TestCase):

    def testRepeat(self):
        # Test Repeat
        seq = SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)])
        seq = SvPkg.repeat(seq, 4).combine(SvPkg.CombineMethod.DROP_BY_POINT)

        self.assertEqual(len(seq), 5)


if __name__ == '__main__':
    unittest.main()

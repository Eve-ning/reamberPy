import unittest
from reamber.algorithms.generate.sv.SvSequence import SvSequence,SvObj


class TestInit(unittest.TestCase):

    def testMixed(self):
        # Quick Init Mixed
        seq = SvSequence([100, (200, 2.0, True), (400, 3.0), SvObj(offset=800, multiplier=5.0, fixed=True)])
        self.assertEqual(len(seq), 4)


if __name__ == '__main__':
    unittest.main()

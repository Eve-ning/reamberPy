import unittest
from reamber.algorithms.generate.sv.SvSequence import SvSequence,SvObj
from reamber.algorithms.generate.sv.SvPkg import SvPkg


class TestInit(unittest.TestCase):
    def test(self):

        t = SvPkg([SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)]),
                   SvSequence([SvObj(100, 3.0), SvObj(200, 4.0)]),
                   SvSequence([SvObj(150, 5.0), SvObj(300, 6.0)])])\
            .combine(combineMethod=SvPkg.CombineMethod.DROP_BY_POINT, combineMethodWindow=1)

        self.assertEqual(len(t), 5)

        t = SvPkg([SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)]),
                   SvSequence([SvObj(100, 3.0), SvObj(200, 4.0)]),
                   SvSequence([SvObj(150, 5.0), SvObj(300, 6.0)])])\
            .combine(combineMethod=SvPkg.CombineMethod.DROP_BY_BOUND, combineMethodWindow=1)

        self.assertEqual(len(t), 4)

        t = SvPkg([SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)]),
                   SvSequence([SvObj(100, 3.0), SvObj(200, 4.0)]),
                   SvSequence([SvObj(150, 5.0), SvObj(300, 6.0)])])\
            .combine(combineMethod=SvPkg.CombineMethod.IGNORE, combineMethodWindow=1)

        self.assertEqual(len(t), 6)

    def testMixed(self):
        # Quick Init Mixed
        seq = SvSequence([100, (200, 2.0, True), (400, 3.0), SvObj(offset=800, multiplier=5.0, fixed=True)])
        self.assertEqual(len(seq), 4)


if __name__ == '__main__':
    unittest.main()

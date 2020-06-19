import unittest
from reamber.algorithms.generate.sv.SvSequence import SvSequence,SvObj


class TestSvSequence(unittest.TestCase):
    def test(self):
        t = SvSequence.combine([SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)]),
                                SvSequence([SvObj(100, 3.0), SvObj(200, 4.0)]),
                                SvSequence([SvObj(150, 5.0), SvObj(300, 6.0)])],
                               combineMethod=SvSequence.CombineMethod.DROP_BY_POINT,
                               combineMethodWindow=1)

        self.assertEqual(len(t), 5)

        t = SvSequence.combine([SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)]),
                                SvSequence([SvObj(100, 3.0), SvObj(200, 4.0)]),
                                SvSequence([SvObj(150, 5.0), SvObj(300, 6.0)])],
                               combineMethod=SvSequence.CombineMethod.DROP_BY_BOUND,
                               combineMethodWindow=1)

        self.assertEqual(len(t), 4)

        t = SvSequence.combine([SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)]),
                                SvSequence([SvObj(100, 3.0), SvObj(200, 4.0)]),
                                SvSequence([SvObj(150, 5.0), SvObj(300, 6.0)])],
                               combineMethod=SvSequence.CombineMethod.IGNORE,
                               combineMethodWindow=1)

        self.assertEqual(len(t), 6)


if __name__ == '__main__':
    unittest.main()

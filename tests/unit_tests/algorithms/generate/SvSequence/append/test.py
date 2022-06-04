import unittest

from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence, SvObj


class TestAppend(unittest.TestCase):
    def test(self):

        t = SvPkg([SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)]),
                   SvSequence([SvObj(100, 3.0), SvObj(200, 4.0)]),
                   SvSequence([SvObj(150, 5.0), SvObj(300, 6.0)])])\
            .combine(combine_method=SvPkg.CombineMethod.DROP_BY_POINT, combine_method_window=1)

        self.assertEqual(len(t), 5)

        t.append_init([(0, 1.0), SvObj(100, 2.0), (1000, 2.0, True), 1000])

        self.assertEqual(len(t), 9)


if __name__ == '__main__':
    unittest.main()

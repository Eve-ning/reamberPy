import unittest

from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence, SvObj


def test_sa():

    t = SvPkg([SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)]),
               SvSequence([SvObj(100, 3.0), SvObj(200, 4.0)]),
               SvSequence([SvObj(150, 5.0), SvObj(300, 6.0)])])\
        .combine(combine_method=SvPkg.CombineMethod.DROP_BY_POINT, combine_method_window=1)

    assert len(t) == 5

    t.append_init([(0, 1.0), SvObj(100, 2.0), (1000, 2.0, True), 1000])

    assert len(t) == 9


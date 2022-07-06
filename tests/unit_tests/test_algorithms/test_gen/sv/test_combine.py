from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence, SvObj


def test_combine():
    t = SvPkg([SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)]),
               SvSequence([SvObj(100, 3.0), SvObj(200, 4.0)]),
               SvSequence([SvObj(150, 5.0), SvObj(300, 6.0)])]) \
        .combine(combine_method=SvPkg.CombineMethod.DROP_BY_POINT,
                 combine_method_window=1)

    assert len(t) == 5

    t = SvPkg([SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)]),
               SvSequence([SvObj(100, 3.0), SvObj(200, 4.0)]),
               SvSequence([SvObj(150, 5.0), SvObj(300, 6.0)])]) \
        .combine(combine_method=SvPkg.CombineMethod.DROP_BY_BOUND,
                 combine_method_window=1)

    assert len(t) == 4

    t = SvPkg([SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)]),
               SvSequence([SvObj(100, 3.0), SvObj(200, 4.0)]),
               SvSequence([SvObj(150, 5.0), SvObj(300, 6.0)])]) \
        .combine(combine_method=SvPkg.CombineMethod.IGNORE,
                 combine_method_window=1)

    assert len(t) == 6

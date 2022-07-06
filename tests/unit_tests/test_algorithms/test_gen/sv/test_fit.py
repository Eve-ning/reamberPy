from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence, SvObj


def test_fit():
    # Test Fitting
    seq = SvSequence([SvObj(0, 0.5), SvObj(50, 1.5), SvObj(100, 1.0)])
    seq = SvPkg.fit(seq, [0, 100, 200, 400, 600]).combine(
        SvPkg.CombineMethod.DROP_BY_POINT)

    assert len(seq) == 9

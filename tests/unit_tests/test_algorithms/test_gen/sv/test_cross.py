import pytest

from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence, SvObj


def test_cross():
    # Test Cross
    seq = SvSequence(
        [SvObj(0, 0.5), SvObj(100, 2.0), SvObj(200, 3.0), SvObj(400, 2.0)])
    seq2 = SvSequence(
        [SvObj(50, 0.1), SvObj(100, 10.0), SvObj(250, 5.0), SvObj(500, 0.3)])
    seq.cross_with(seq2, inplace=True)

    assert seq[0].multiplier == pytest.approx(0.5)
    assert seq[1].multiplier == pytest.approx(20.0)
    assert seq[2].multiplier == pytest.approx(30.0)
    assert seq[3].multiplier == pytest.approx(10.0)


def test_mutual_cross():
    # Test Mutual Cross
    seq1 = SvSequence(
        [SvObj(0, 0.5), SvObj(100, 2.0), SvObj(200, 3.0), SvObj(400, 2.0)])
    seq2 = SvSequence(
        [SvObj(50, 0.1), SvObj(100, 10.0), SvObj(250, 5.0), SvObj(500, 0.2)])
    seq = SvPkg.cross_mutual_with(seq1, seq2).combine(
        SvPkg.CombineMethod.DROP_BY_POINT)

    assert seq[0].multiplier == pytest.approx(0.5)
    assert seq[1].multiplier == pytest.approx(0.05)
    assert seq[2].multiplier == pytest.approx(20.0)
    assert seq[3].multiplier == pytest.approx(30.0)
    assert seq[4].multiplier == pytest.approx(15.0)
    assert seq[5].multiplier == pytest.approx(10.0)
    assert seq[6].multiplier == pytest.approx(0.4)

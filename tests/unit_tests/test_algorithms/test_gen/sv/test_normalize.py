import pytest

from reamber.algorithms.generate.sv.SvSequence import SvSequence


def test_control():
    seq = SvSequence([0, (500, 1.5, True), 1000])
    seq.normalize_to(inplace=True)
    assert seq[0].multiplier == pytest.approx(0.5)


def test_complex():
    seq = SvSequence(
        [0, (500, 1.5, True), (700, 0.75, True), (800, 1.5, False), 1000])
    seq.normalize_to(inplace=True)
    assert seq[0].multiplier == pytest.approx(0.78125)
    assert seq[3].multiplier == pytest.approx(1.171875)


def test_ignore_fixed():
    seq = SvSequence([0, (500, 1.5, True), 1000])
    seq.normalize_to(inplace=True, ignore_fixed=True)
    assert seq[0].multiplier == pytest.approx(0.8)
    assert seq[1].multiplier == pytest.approx(1.2)


def test_bad_min():
    seq = SvSequence([0, (500, 2.1, True), 1000])
    with pytest.raises(AssertionError):
        seq.normalize_to(inplace=True, min_allowable=0)


def test_bad_max():
    seq = SvSequence([0, (500, 0.5, True), 1000])
    with pytest.raises(AssertionError):
        seq.normalize_to(inplace=True, max_allowable=1.2)

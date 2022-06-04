import pandas as pd

from reamber.base import Hold


def hold():
    return Hold(offset=1000, column=1, length=1000)


def test_type(hold):
    assert isinstance(hold.data, pd.Series)


def test_eq(hold):
    assert Hold(offset=1000, column=1, length=1000) == hold
    assert Hold(offset=1000, column=1, length=2000) != hold


def test_length(hold):
    assert 1000 == hold.length


def test_tail_offset(hold):
    assert 2000 == hold.tail_offset


def test_deepcopy(hold):
    assert hold is not Hold(offset=1000, column=1, length=1000)
    assert hold is not hold.deepcopy()
    hold_copy = hold
    assert hold_copy is hold


def test_length_op(hold):
    assert 1000 == hold.length
    hold.length *= 2
    assert 2000 == hold.length
    assert 3000 == hold.tail_offset
    # An odd occurrence, but we support negative lengths.
    hold.length = -1000
    assert -1000 == hold.length
    assert 0 == hold.tail_offset

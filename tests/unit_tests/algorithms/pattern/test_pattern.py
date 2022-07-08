import pytest

from reamber.algorithms.pattern import Pattern


@pytest.fixture
def pattern(columns, offsets, types):
    return Pattern(columns, offsets, types)


def test_pattern_init(columns, offsets, types):
    p = Pattern(columns, offsets, types)
    assert all(p.ar['column'] == columns)
    assert all(p.ar['offset'] == offsets)
    assert all(p.ar['type'] == types)


def test_pattern_from_nl(hit_list, hold_list, columns, offsets, types):
    p = Pattern.from_note_lists([hit_list, hold_list])
    assert set(p.ar['column']) == set(columns)
    assert set(p.ar['offset']) == set(offsets)
    assert set(p.ar['type']) == set(types)


def test_pattern_h_mask(pattern):
    assert all(pattern.h_mask(1, 1) == [True, True, True, True, True, False])
    assert all(pattern.h_mask(0, 1) == [True, True, True, False, False, False])


def test_pattern_v_mask(pattern):
    assert all(pattern.v_mask(100, 100, False) ==
               [False, False, True, True, True, True])
    assert all(pattern.v_mask(100, 100, True) ==
               [False, False, True, True, False, True])
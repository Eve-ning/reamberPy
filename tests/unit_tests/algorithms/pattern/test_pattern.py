from reamber.algorithms.pattern import Pattern


def test_pattern_init(columns, offsets, types):
    p = Pattern(columns, offsets, types)
    assert all(p.df['column'] == columns)
    assert all(p.df['offset'] == offsets)
    assert all(p.df['type'] == types)


def test_pattern_from_nl(hit_list, hold_list, columns, offsets, types):
    p = Pattern.from_note_lists([hit_list, hold_list])
    assert set(p.df['column']) == set(columns)
    assert set(p.df['offset']) == set(offsets)
    assert set(p.df['type']) == set(types)


def test_pattern_h_mask(pattern):
    assert all(pattern.h_mask(pattern.df, 1, 1) ==
               [True, True, True, True, True, False, True])
    assert all(pattern.h_mask(pattern.df, 0, 1) ==
               [True, True, True, False, False, False, False])


def test_pattern_v_mask(pattern):
    assert all(pattern.v_mask(pattern.df, 100, 100, False) ==
               [False, False, True, True, True, True, False])
    assert all(pattern.v_mask(pattern.df, 100, 100, True) ==
               [False, False, True, True, False, True, False])

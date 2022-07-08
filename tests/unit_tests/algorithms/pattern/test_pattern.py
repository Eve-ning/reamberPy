from reamber.algorithms.pattern import Pattern


def test_pattern_init(columns, offsets, types):
    p = Pattern(columns, offsets, types)


def test_pattern_from_nl(hit_list, hold_list):
    p = Pattern.from_note_lists([hit_list, hold_list])

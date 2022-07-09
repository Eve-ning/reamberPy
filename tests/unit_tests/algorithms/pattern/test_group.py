import pytest


@pytest.mark.parametrize(
    'v_window, avoid_jack, group_offsets',
    [
        [0, True, [[0, 0], [100, 100], [200, 200], [300]]],
        [100, False, [[0, 0, 100, 100], [200, 200, 300]]],
        [100, True, [[0, 0, 100], [100, 200, 200], [300]]],
        [200, True, [[0, 0, 100, 200], [100, 200], [300]]],
    ]
)
def test_pattern_group(pattern, v_window, avoid_jack, group_offsets):
    pgs = pattern.group(v_window, None, avoid_jack)
    for e, g in enumerate(group_offsets):
        assert all(pgs[e].offset == g), (pgs[e].offset, g)

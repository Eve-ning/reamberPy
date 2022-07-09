import pytest

from reamber.algorithms.pattern.filters.PtnFilter import PtnFilterChord, \
    PtnFilterCombo

from reamber.algorithms.pattern.combos import PtnCombo


@pytest.mark.parametrize(
    'size, shapes',
    [
        [2, [4, 4]],
        [3, [16]],
    ]
)
def test_pattern_combo(size, shapes, pattern):
    chord_filter = PtnFilterChord.create(chord_sizes=[[2, 2]], keys=4,).filter
    combos = PtnCombo(pattern.group()).combinations(
        size=size,
        make_size2=True,
        chord_filter=chord_filter
    )
    for shape, combo in zip(shapes, combos):
        assert combo.shape[0] == shape




def test_combo():
    c = PtnFilterCombo.create(combos=[[0, 0, 0], [1, 1, 1]], keys=4)
    d = PtnFilterCombo.create(combos=[[0, 0, 0], [2, 2, 2]], keys=4)
    e = c | d
    assert e.ar.shape == (3, 3)

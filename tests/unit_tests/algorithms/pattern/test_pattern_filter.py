import pytest

from reamber.algorithms.pattern.combos import PtnCombo
from reamber.algorithms.pattern.filters import PtnFilterType
from reamber.algorithms.pattern.filters.PtnFilter import PtnFilterChord, \
    PtnFilterCombo
from reamber.base.Hit import Hit
from reamber.base.Hold import HoldTail


@pytest.mark.parametrize(
    'size, chord_sizes, shapes',
    [
        [2, [[2, 2]], [4, 4]],
        [3, [[2, 2, 2]], [16]],
    ]
)
def test_pattern_chord(size, chord_sizes, shapes, pattern):
    chord_filter = PtnFilterChord.create(chord_sizes=chord_sizes,
                                         keys=4, ).filter
    combos = PtnCombo(pattern.group()).combinations(
        size=size,
        make_size2=True,
        chord_filter=chord_filter
    )
    for shape, combo in zip(shapes, combos):
        assert combo.shape[0] == shape


@pytest.mark.parametrize(
    'size, combos, shapes',
    [
        [2, [[1, 2]], [1, 1]],
        [3, [[1, 2, 2]], [2, 2]],
    ]
)
def test_pattern_combo(size, combos, shapes, pattern):
    combo_filter = PtnFilterCombo.create(combos=combos, keys=4).filter
    combos = PtnCombo(pattern.group()).combinations(
        size=size,
        make_size2=True,
        combo_filter=combo_filter
    )
    for shape, combo in zip(shapes, combos):
        assert combo.shape[0] == shape


@pytest.mark.parametrize(
    'size, types_, shapes',
    [
        [2, [[Hit, Hit]], [2, 1, 1]],
        [2, [[HoldTail, Hit]], [1]],
    ]
)
def test_pattern_type(size, types_, shapes, pattern):
    type_filter = PtnFilterType.create(types=types_).filter
    combos = PtnCombo(pattern.group()).combinations(
        size=size,
        make_size2=True,
        type_filter=type_filter
    )
    for shape, combo in zip(shapes, combos):
        assert combo.shape[0] == shape

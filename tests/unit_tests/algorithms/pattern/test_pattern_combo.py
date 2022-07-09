import pytest

from reamber.algorithms.pattern.combos import PtnCombo


@pytest.mark.parametrize(
    'size, shapes',
    [
        [2, [4, 4, 2]],
        [3, [16, 8]],
        [4, [24]],
    ]
)
def test_pattern_combo(size, shapes, pattern):
    combos = PtnCombo(pattern.group()).combinations(size=size, make_size2=True)
    for shape, combo in zip(shapes, combos):
        assert combo.shape[0] == shape

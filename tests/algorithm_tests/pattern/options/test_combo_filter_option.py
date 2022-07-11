import numpy as np

from reamber.algorithms.pattern.filters import PtnFilterCombo


def test_combo():
    assert np.all(
        PtnFilterCombo.create(
            combos=[[1, 1, 1]], keys=2,
        ).ar == np.array([1, 1, 1])
    )


def test_combo_repeat():
    assert np.all(
        PtnFilterCombo.create(
            combos=[[1, 1, 1]], keys=3,
            options=PtnFilterCombo.Option.REPEAT
        ).ar == np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    )


def test_combo_h_mirror():
    assert np.all(
        PtnFilterCombo.create(
            combos=[[0, 0, 0]], keys=3,
            options=PtnFilterCombo.Option.HMIRROR
        ).ar == np.array([[0, 0, 0], [2, 2, 2]])
    )


def test_combo_v_mirror():
    assert np.all(
        PtnFilterCombo.create(
            combos=[[0, 2, 2]], keys=3,
            options=PtnFilterCombo.Option.VMIRROR
        ).ar == np.array([[0, 2, 2], [2, 2, 0]])
    )


def test_combo_h_v_mirror():
    assert np.all(
        PtnFilterCombo.create(
            combos=[[0, 2, 2]], keys=3,
            options=PtnFilterCombo.Option.HMIRROR |
                    PtnFilterCombo.Option.VMIRROR
        ).ar == np.array([[0, 0, 2], [0, 2, 2], [2, 0, 0], [2, 2, 0]])
    )


def test_combo_h_v_mirror_repeat():
    assert np.all(
        PtnFilterCombo.create(
            combos=[[0, 2, 2]], keys=4,
            options=PtnFilterCombo.Option.HMIRROR |
                    PtnFilterCombo.Option.VMIRROR |
                    PtnFilterCombo.Option.REPEAT
        ).ar == np.array([[0, 0, 2], [0, 2, 2], [1, 1, 3], [1, 3, 3],
                          [2, 0, 0], [2, 2, 0], [3, 1, 1], [3, 3, 1], ])
    )

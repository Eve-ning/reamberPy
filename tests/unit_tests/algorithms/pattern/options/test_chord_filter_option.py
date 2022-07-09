import numpy as np

from reamber.algorithms.pattern.filters.PtnFilter import PtnFilterChord


def test_chord():
    assert np.all(
        PtnFilterChord.create(
            chord_sizes=[[1, 1, 1]], keys=2,
        ).ar == np.array([1, 1, 1])
    )


def test_chord_and_higher():
    assert np.all(
        PtnFilterChord.create(
            chord_sizes=[[1, 2]], keys=2,
            options=PtnFilterChord.Option.AND_HIGHER
        ).ar == np.array([[1, 2], [2, 2]])
    )


def test_chord_and_lower():
    assert np.all(
        PtnFilterChord.create(
            chord_sizes=[[2, 1]], keys=2,
            options=PtnFilterChord.Option.AND_LOWER
        ).ar == np.array([[1, 1], [2, 1]])
    )


def test_chord_any_order():
    assert np.all(
        PtnFilterChord.create(
            chord_sizes=[[2, 1, 1]], keys=2,
            options=PtnFilterChord.Option.ANY_ORDER
        ).ar == np.array([[1, 1, 2], [1, 2, 1], [2, 1, 1]])
    )

def test_chord_and_lower_any_order():
    assert np.all(
        PtnFilterChord.create(
            chord_sizes=[[2, 1]], keys=2,
            options=PtnFilterChord.Option.AND_LOWER |
                    PtnFilterChord.Option.ANY_ORDER
        ).ar == np.array([[1, 1], [1, 2], [2, 1]])
    )


def test_chord_and_higher_any_order():
    assert np.all(
        PtnFilterChord.create(
            chord_sizes=[[1, 2]], keys=2,
            options=PtnFilterChord.Option.AND_HIGHER |
                    PtnFilterChord.Option.ANY_ORDER
        ).ar == np.array([[1, 2], [2, 1], [2, 2]])
    )

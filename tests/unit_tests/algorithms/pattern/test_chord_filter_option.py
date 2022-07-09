import numpy as np

from reamber.algorithms.pattern.filters.PtnFilter import PtnFilterChord


def test_chord():
    assert (
        PtnFilterChord.create(
            chord_sizes=[[1, 1, 1]], keys=2,
        ).ar == np.array([1, 1, 1])
    ).all()


def test_chord_and_higher():
    assert (
        PtnFilterChord.create(
            chord_sizes=[[1, 1]], keys=2,
            options=PtnFilterChord.Option.AND_HIGHER
        ).ar == np.array([[1, 1], [1, 2], [2, 1], [2, 2]])
    ).all()


def test_chord_and_lower():
    assert (
        PtnFilterChord.create(
            chord_sizes=[[2, 2]], keys=2,
            options=PtnFilterChord.Option.AND_LOWER
        ).ar == np.array([[1, 1], [1, 2], [2, 1], [2, 2]])
    ).all()


def test_chord_any_order():
    assert (
        PtnFilterChord.create(
            chord_sizes=[[2, 1, 1]], keys=2,
            options=PtnFilterChord.Option.ANY_ORDER
        ).ar == np.array([[1, 1, 2], [1, 2, 1], [2, 1, 1]])
    ).all()

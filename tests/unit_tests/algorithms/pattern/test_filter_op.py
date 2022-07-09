from reamber.algorithms.pattern.filters.PtnFilter import PtnFilterChord, \
    PtnFilterCombo


def test_and_op():
    a = PtnFilterChord.create(
        chord_sizes=[[1, 1, 1]], keys=4,
        options=PtnFilterChord.Option.AND_HIGHER |
                PtnFilterChord.Option.ANY_ORDER
    )

    b = PtnFilterChord.create(
        chord_sizes=[[3, 3, 3]], keys=4,
        options=PtnFilterChord.Option.AND_LOWER |
                PtnFilterChord.Option.ANY_ORDER
    )
    c = a & b
    assert c.ar.shape == (27, 3)


def test_or_op():
    c = PtnFilterCombo.create(combos=[[0, 0, 0], [1, 1, 1]], keys=4)
    d = PtnFilterCombo.create(combos=[[0, 0, 0], [2, 2, 2]], keys=4)
    e = c | d
    assert e.ar.shape == (3, 3)

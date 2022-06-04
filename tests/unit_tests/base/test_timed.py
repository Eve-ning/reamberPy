from reamber.base import Timed


def test__gt__(rand):
    assert Timed(offset=rand) < Timed(offset=rand + 1)


def test__lt__(rand):
    assert Timed(offset=rand + 1) > Timed(offset=rand)


def test_sort(randintp):
    objs = sorted([Timed(i) for i in range(randintp)[::-1]])
    assert [Timed(i) for i in range(randintp)] == objs

from reamber.base import Timed


def test_eq(rand):
    assert Timed(offset=rand) == Timed(offset=rand)


def test__gt__(rand):
    assert Timed(offset=rand) < Timed(offset=rand + 1)


def test_op_lt(rand):
    assert Timed(offset=rand + 1) > Timed(offset=rand)


def test_deepcopy():
    assert Timed(offset=1000) is not Timed(offset=1000)
    t = Timed(offset=1000)
    assert t is not t.deepcopy()
    t2 = t
    assert t == t2


def test_sort(randintp):
    objs = sorted([Timed(i) for i in range(randintp)[::-1]])
    assert [Timed(i) for i in range(randintp)] == objs

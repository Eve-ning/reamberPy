from reamber.base import Map
from reamber.base.lists.notes import HitList, HoldList


def test_type(map_set):
    assert all(isinstance(m, Map) for m in map_set)


def test_stack(offsets, randintpm, map_set):
    s = map_set.stack()
    s.offset += randintpm

    for m in map_set:
        assert all(offsets + randintpm == m[HitList][0].offset)
        assert all(offsets + randintpm == m[HoldList][0].offset)


def test_stack_inline(map_set, offsets, randintpm):
    """ Checks if inline stacking works """
    map_set.stack().offset += randintpm
    for m in map_set:
        assert all(offsets + randintpm == m[HitList][0].offset)
        assert all(offsets + randintpm == m[HoldList][0].offset)


def test_rate(map_set, offsets, randintp, hold_lengths):
    r = randintp
    for m in map_set.rate(1 / randintp):
        assert all(offsets * r == m[HitList][0].offset)
        assert all(offsets * r == m[HoldList][0].offset)
        assert all(
            offsets * r + hold_lengths * r == m[HoldList][0].tail_offset
        )


def test_deepcopy(map_set):
    assert map_set is not map_set.deepcopy()


def test_getitem(map_set):
    assert all([isinstance(m, Map) for m in map_set[:]])
    assert isinstance(map_set[0], Map)
    assert all([isinstance(m, HitList) for m in map_set[HitList]])

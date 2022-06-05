from reamber.base import Map
from reamber.base.lists import BpmList
from reamber.base.lists.notes import HitList, HoldList
from reamber.base.lists.notes.NoteList import NoteList


def test_getitem(map):
    assert isinstance(map[NoteList][0], (HitList, HoldList))
    assert isinstance(map[NoteList][1], (HitList, HoldList))
    assert isinstance(map[HitList][0], HitList)
    assert isinstance(map[HoldList][0], HoldList)
    assert isinstance(map[BpmList][0], BpmList)


def test_rate(randintp, offsets, map, hold_lengths):
    r = randintp
    m = map.rate(1 / r)
    assert all(offsets * r == m[HitList][0].offset)
    assert all(offsets * r == m[HoldList][0].offset)
    assert all(offsets * r + hold_lengths * r == m[HoldList][0].tail_offset)


def test_deepcopy(map):
    assert map is not map.deepcopy()


def test_stack_mutate(map, randintp, offsets, bpm_bpms, hold_lengths):
    s = map.stack()
    r = randintp
    s.offset *= r

    assert all(offsets * r == map[HitList][0].offset)
    assert all(offsets * r == map[HoldList][0].offset)
    assert all(offsets * r == map[BpmList][0].offset)

    s.bpm *= r
    assert all(bpm_bpms * r == map[BpmList][0].bpm)

    s.length *= r
    assert all(hold_lengths * r == map[HoldList][0].length)


def test_empty_handling():
    """ This ensures that the uncalled classes are still initialized. """
    m = Map()
    _ = m[HitList]
    _ = m[HoldList]


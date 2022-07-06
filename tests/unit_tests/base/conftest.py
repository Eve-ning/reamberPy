import numpy as np
import pytest

from reamber.base import Bpm, Hold, Map, MapSet, Timed, Note, Hit
from reamber.base.lists import BpmList, TimedList
from reamber.base.lists.notes import HoldList, NoteList, HitList


@pytest.fixture
def timeds(offsets):
    return [Timed(offset) for offset in offsets]


@pytest.fixture
def timed_list(timeds):
    return TimedList(timeds)


@pytest.fixture
def bpms(offsets, bpm_bpms, bpm_metronomes):
    return [Bpm(offset=o, bpm=b, metronome=m) for o, b, m in
            zip(offsets, bpm_bpms, bpm_metronomes)]


@pytest.fixture
def bpm_list(bpms):
    return BpmList(bpms)


@pytest.fixture
def note_list(offsets, columns):
    return NoteList(
        [Note(offset=o, column=c) for o, c in zip(offsets, columns)])


@pytest.fixture
def hold_lengths():
    return np.asarray([50, 50, 50, 50])


@pytest.fixture
def holds(offsets, columns, hold_lengths):
    return [Hold(offset=o, column=c, length=l) for o, c, l in
            zip(offsets, columns, hold_lengths)]


@pytest.fixture
def hold_list(holds) -> HoldList:
    return HoldList(holds)


@pytest.fixture
def hits(offsets, columns):
    return [Hit(offset=o, column=c) for o, c in zip(offsets, columns)]


@pytest.fixture
def hit_list(hits) -> HitList:
    return HitList(hits)


@pytest.fixture
def map(hit_list, hold_list, bpm_list) -> Map:
    map_ = Map()
    map_.hits = hit_list
    map_.holds = hold_list
    map_.bpms = bpm_list
    return map_


@pytest.fixture
def map_set(map) -> MapSet:
    return MapSet([map, map.deepcopy()])

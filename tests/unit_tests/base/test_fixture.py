import os

import numpy as np
import pytest

from reamber.base import Bpm, Hit, Hold, Map, MapSet
from reamber.base.lists import BpmList
from reamber.base.lists.notes import HitList, HoldList



@pytest.fixture(scope='package')
def bpms():
    bpm_offsets = np.asarray([0, 800, 1600, 2500])
    bpm_bpms = np.asarray([300, 300, 200, 200])
    bpm_metronomes = np.asarray([4, 4, 3, 5])
    return [Bpm(offset=o, bpm=b, metronome=m) for o, b, m in
            zip(bpm_offsets, bpm_bpms, bpm_metronomes)]


@pytest.fixture(scope='package')
def bpm_list(bpms):
    return BpmList(bpms)


@pytest.fixture(scope='package')
def hits():
    hit_offsets = np.asarray(
        [0, 200, 300, 400, 500, 600, 900, 1000, 1400, 1600, 2200, 2350])
    hit_columns = np.asarray([0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3])

    return [Hit(offset=o, column=c) for o, c in zip(hit_offsets, hit_columns)]

@pytest.fixture(scope='package')
def hit_list(hits) -> HitList:
    return HitList(hits)


@pytest.fixture(scope='package')
def hold_list() -> HoldList:
    hold_offsets = np.asarray([0, 100, 300, 600, 1000, 1500])
    hold_columns = np.asarray([2, 3, 0, 3, 1, 0])
    hold_lengths = np.asarray([200, 100, 100, 300, 300, 1000])

    holds = [Hold(offset=o, column=c, length=l) for o, c, l in
             zip(hold_offsets, hold_columns, hold_lengths)]
    return HoldList(holds)


@pytest.fixture(scope='package')
def map(hit_list, hold_list, bpm_list) -> Map:
    map_ = Map()
    map_.hits = hit_list
    map_.holds = hold_list
    map_.bpms = bpm_list
    return map_


@pytest.fixture(scope='package')
def map_set(map) -> MapSet:
    map2 = map.deepcopy()

    return MapSet([map, map2])

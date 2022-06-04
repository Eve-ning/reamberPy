import unittest

import numpy as np
import pytest

from reamber.base import Bpm, Hit, Hold, Map, MapSet
from reamber.base.lists import BpmList
from reamber.base.lists.notes import HitList, HoldList
from .test_fixture import *




def test_type(map_set):
    assert isinstance(map_set.maps, list)

def test_stack(hit_list, hold_list, map_set):
    s = map_set.stack()

    assert hit_list.offset.tolist() == map_set.maps[0][HitList][0].offset.tolist()
    assert hold_list.offset.tolist() == map_set.maps[0][HoldList][0].offset.tolist()
    assert hit_list.offset.tolist() == map_set.maps[1][HitList][0].offset.tolist()
    assert hold_list.offset.tolist() == map_set.maps[1][HoldList][0].offset.tolist()

    s.offset += 1000

    assert (hit_list.offset + 1000).tolist() == map_set.maps[0][HitList][0].offset.tolist()
    assert (hold_list.offset + 1000).tolist() == map_set.maps[0][HoldList][0].offset.tolist()
    assert (hit_list.offset + 1000).tolist() == map_set.maps[1][HitList][0].offset.tolist()
    assert (hold_list.offset + 1000).tolist() == map_set.maps[1][HoldList][0].offset.tolist()

def test_stack_loop(self):
    for m in map_set:
        stack = m.stack(['hits'])
        stack.loc[stack.offset < 1000, 'column'] += 1

    assert hit_columns[0] + 1 == map_set[0].hits.column[0]
    assert hold_columns[0] == map_set[0].holds.column[0]
    assert hit_columns[-1] == map_set[0].hits.column.tolist()[-1]
    assert hold_columns[-1] == map_set[0].holds.column.tolist()[-1]

def test_stack_offset(self):
    s = map_set.stack()
    s.offset *= 2
    assert (hit_list.offset * 2).tolist() == \
           map_set.maps[0][HitList][0].offset.tolist()
    assert (hold_list.offset * 2).tolist() == \
           map_set.maps[0][HoldList][0].offset.tolist()
    assert ((hold_list.offset * 2) + hold_lengths).tolist() == \
           map_set.maps[0][HoldList][0].tail_offset.tolist()
    assert (hit_list.offset * 2).tolist() == \
           map_set.maps[1][HitList][0].offset.tolist()
    assert (hold_list.offset * 2).tolist() == \
           map_set.maps[1][HoldList][0].offset.tolist()
    assert ((hold_list.offset * 2) + hold_lengths).tolist() == \
           map_set.maps[1][HoldList][0].tail_offset.tolist()

def test_stack_column(self):
    s = map_set.stack()
    s.column *= 2
    assert (hit_columns * 2).tolist() == \
           map_set.maps[0][HitList][0].column.tolist()
    assert (hold_columns * 2).tolist() == \
           map_set.maps[0][HoldList][0].column.tolist()
    assert (hit_columns * 2).tolist() == \
           map_set.maps[1][HitList][0].column.tolist()
    assert (hold_columns * 2).tolist() == \
           map_set.maps[1][HoldList][0].column.tolist()

def test_stack_inline(self):
    """ Checks if inline stacking works """
    map_set.stack().column *= 2
    assert (hit_columns * 2).tolist() == \
           map_set[0][HitList][0].column.tolist()
    assert (hold_columns * 2).tolist() == \
           map_set[0][HoldList][0].column.tolist()
    assert (hit_columns * 2).tolist() == \
           map_set[1][HitList][0].column.tolist()
    assert (hold_columns * 2).tolist() == \
           map_set[1][HoldList][0].column.tolist()

def test_rate(self):
    ms = map_set.rate(0.5)
    assert (hit_list.offset * 2).tolist() == \
           ms[0][HitList][0].offset.tolist()
    assert (hold_list.offset * 2).tolist() == \
           ms[0][HoldList][0].offset.tolist()
    assert (hold_list.offset * 2 + hold_lengths * 2).tolist() == \
           ms[0][HoldList][0].tail_offset.tolist()
    assert (hit_list.offset * 2).tolist() == \
           ms[1][HitList][0].offset.tolist()
    assert (hold_list.offset * 2).tolist() == \
           ms[1][HoldList][0].offset.tolist()
    assert (hold_list.offset * 2 + hold_lengths * 2).tolist() == \
           ms[1][HoldList][0].tail_offset.tolist()

def test_deepcopy(self):
    ms = map_set.deepcopy()
    ms.stack().column *= 2

    assert (hit_columns * 2).tolist() == \
           ms[0][HitList][0].column.tolist()
    assert (hold_columns * 2).tolist() == \
           ms[0][HoldList][0].column.tolist()
    assert (hit_columns * 2).tolist() == \
           ms[1][HitList][0].column.tolist()
    assert (hold_columns * 2).tolist() == \
           ms[1][HoldList][0].column.tolist()

    assert hit_columns.tolist() == \
           map_set[0][HitList][0].column.tolist()
    assert hold_columns.tolist() == \
           map_set[0][HoldList][0].column.tolist()
    assert hit_columns.tolist() == \
           map_set[1][HitList][0].column.tolist()
    assert hold_columns.tolist() == \
           map_set[1][HoldList][0].column.tolist()



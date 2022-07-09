from dataclasses import dataclass, field
from typing import Dict

import pytest

from reamber.base import Map
from reamber.base.Property import map_props
from reamber.base.lists import TimedList
from tests.unit_tests.base.inheritance.test_timed_inherit import TimedInherit


@map_props()
@dataclass
class MapInherit(Map[TimedInherit, TimedInherit, TimedInherit, TimedInherit]):
    _props = dict(timed=TimedList)
    objs: Dict[str, TimedList] = \
        field(init=False, default_factory=lambda: dict(timed=TimedList([])))


@pytest.fixture
def map() -> MapInherit:
    return MapInherit()


def test_map_prop_get(map):
    assert isinstance(map.timed, TimedList)


def test_map_prop_set(map):
    map.timed = TimedList([])
    test_map_prop_get(map)

import pytest

from reamber.algorithms.pattern import Pattern
from reamber.base.Hit import Hit
from reamber.base.Hold import Hold, HoldTail
from reamber.base.lists.notes.HitList import HitList
from reamber.base.lists.notes.HoldList import HoldList

"""
Pattern
+---+---+---+---+                       
|         o     | 300 ms                   
|         T   o | 200 ms                   
|     o   H     | 100 ms              
| o   o         |   0 ms    
+---+---+---+---+                       
"""


@pytest.fixture
def columns():
    return [0, 1, 1, 2, 2, 3, 2]


@pytest.fixture
def offsets():
    return [0, 0, 100, 100, 200, 200, 300]


@pytest.fixture
def types():
    return [Hit, Hit, Hit, Hold, HoldTail, Hit, Hit]


@pytest.fixture
def hit_list():
    return HitList([Hit(0, 0), Hit(0, 1), Hit(100, 1), Hit(200, 3),
                    Hit(300, 2)])


@pytest.fixture
def hold_list():
    return HoldList([Hold(100, 2, 100)])


@pytest.fixture
def pattern(columns, offsets, types):
    return Pattern(columns, offsets, types)

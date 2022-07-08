import pytest

from reamber.base.Hit import Hit
from reamber.base.Hold import Hold, HoldTail
from reamber.base.lists.notes.HitList import HitList
from reamber.base.lists.notes.HoldList import HoldList

"""
Pattern
+---+---+---+---+                       
|         T   o | 200 ms                   
|     o   H     | 100 ms              
| o   o         |   0 ms    
+---+---+---+---+                       
"""

@pytest.fixture
def columns():
    return [0, 1, 1, 2, 2, 3]


@pytest.fixture
def offsets():
    return [0, 0, 100, 100, 200, 200]


@pytest.fixture
def types():
    return [Hit, Hit, Hit, Hold, HoldTail, Hit]


@pytest.fixture
def hit_list():
    return HitList([Hit(0, 0), Hit(1, 0), Hit(1, 100), Hit(3, 200)])


@pytest.fixture
def hold_list():
    return HoldList([Hold(100, 2, 100)])

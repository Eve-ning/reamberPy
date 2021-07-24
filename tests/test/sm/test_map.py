import os
import unittest

import pytest

from reamber.bms.lists.BMSBpmList import BMSBpmList
from reamber.bms.lists.notes.BMSHitList import BMSHitList
from reamber.bms.lists.notes.BMSHoldList import BMSHoldList
from reamber.sm.lists.notes import SMHitList, SMHoldList, SMMineList, SMLiftList, SMRollList, SMFakeList, SMKeySoundList
from tests.test.bms.test_fixture import bms_map
from tests.test.sm.test_fixture import sm_mapset

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# MAP_READ = os.path.join(THIS_DIR, 'searoad.bml')
# MAP_WRITE_EXP = os.path.join(THIS_DIR, 'map_write_expected.osu')
# MAP_WRITE = os.path.join(THIS_DIR, 'map_write.osu')
from reamber.sm.SMMapSet import SMMapSet
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *

# @profile
def test_type(sm_mapset):
    assert isinstance(sm_mapset[0].hits, SMHitList)
    assert isinstance(sm_mapset[0].holds, SMHoldList)
    assert isinstance(sm_mapset[0].mines, SMMineList)
    assert isinstance(sm_mapset[0].lifts, SMLiftList)
    assert isinstance(sm_mapset[0].rolls, SMRollList)
    assert isinstance(sm_mapset[0].fakes, SMFakeList)
    assert isinstance(sm_mapset[0].keysounds, SMKeySoundList)


# @profile
def test_draw(sm_mapset):
    pf = PlayField(sm_mapset.maps[0]) \
         + PFDrawBeatLines([1]) \
         + PFDrawNotes()
    pf.export_fold(max_height=2000).save("sm.png")

def test_describe(bms_map):
    bms_map.describe()

def test_meta(bms_map):
    assert bms_map.title == b'searoad tracks =side blue= (LN-Applied)'
    assert bms_map.artist == b'sasakure.UK / obj:moya'
    assert bms_map.version == b'16'

def test_deepcopy(bms_map):
    m = bms_map.deepcopy()
    assert m is not bms_map
    test_meta(m)

def test_stack_mutate(bms_map):
    original = bms_map.hits[0].sample
    bms_map.stack.sample += b'_'
    assert original + b'_' == bms_map.hits[0].sample
    with pytest.raises(TypeError): bms_map.stack.sample += 1


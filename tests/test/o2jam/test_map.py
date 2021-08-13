import os

import numpy as np
import pytest

from reamber.o2jam import O2JMap
from reamber.o2jam.lists.O2JBpmList import O2JBpmList
from reamber.o2jam.lists.notes.O2JHitList import O2JHitList
from reamber.o2jam.lists.notes.O2JHoldList import O2JHoldList
from tests.test.o2jam.test_fixture import o2j_mapset

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

MAP_WRITE_EXP = os.path.join(THIS_DIR, 'map_write_expected.sm')
MAP_WRITE = os.path.join(THIS_DIR, 'map_write.sm')

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *


def test_mapset_loop(o2j_mapset):
    for m in o2j_mapset:
        assert isinstance(m, O2JMap)
        assert isinstance(m.hits, O2JHitList)
        assert isinstance(m.holds, O2JHoldList)
        assert isinstance(m.bpms, O2JBpmList)

def test_counts(o2j_mapset):
    assert len(o2j_mapset[0].hits)  == 299
    assert len(o2j_mapset[0].holds) == 23
    assert len(o2j_mapset[0].bpms) == 23
    assert len(o2j_mapset[1].hits)  == 455
    assert len(o2j_mapset[1].holds) == 41
    assert len(o2j_mapset[1].bpms) == 23
    assert len(o2j_mapset[2].hits)  == 554
    assert len(o2j_mapset[2].holds) == 39
    assert len(o2j_mapset[2].bpms) == 25

def test_draw(o2j_mapset):
    pf = PlayField(o2j_mapset.maps[1], padding=0) \
         + PFDrawBeatLines() \
         + PFDrawNotes() \
         + PFDrawBpm()
    pf.export_fold(max_height=1200).save("o2j.png")

def test_describe(o2j_mapset):
    o2j_mapset.describe()

def test_meta(o2j_mapset):
    assert o2j_mapset.artist             == 'BeautifulDay '
    assert o2j_mapset.bmp_size           == 19256
    assert o2j_mapset.bpm                == 130.0
    assert o2j_mapset.cover_offset       == 198268
    assert o2j_mapset.cover_size         == 214025
    assert o2j_mapset.creator            == 'Impact Line'
    assert o2j_mapset.duration           == [121, 123, 121]
    assert o2j_mapset.encode_version     == pytest.approx(2.9)
    assert o2j_mapset.event_count        == [602, 656, 677]
    assert o2j_mapset.genre              == 2
    assert o2j_mapset.level              == [4, 8, 9, 0]
    assert o2j_mapset.measure_count      == [62, 63, 62]
    assert o2j_mapset.note_count         == [345, 537, 632]
    assert o2j_mapset.note_offset        == [300, 70428, 133652]
    assert o2j_mapset.ojm_file           == 'o2ma178.ojm'
    assert o2j_mapset.old_encode_version == 29
    assert o2j_mapset.old_file_version   == 0
    assert o2j_mapset.old_genre          == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
    assert o2j_mapset.old_song_id        == 178
    assert o2j_mapset.package_count      == [342, 343, 325]
    assert o2j_mapset.signature          == 'ojn'
    assert o2j_mapset.song_id            == 178
    assert o2j_mapset.title              == 'Fly Magpie!'

def test_deepcopy(o2j_mapset):
    m = o2j_mapset.deepcopy()
    assert m is not o2j_mapset
    test_meta(m)

def test_rate(o2j_mapset):
    sms = o2j_mapset.rate(0.5)
    assert np.all(o2j_mapset.stack().offset.min() * 2 == sms.stack().offset.min())

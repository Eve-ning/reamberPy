import os

import numpy as np

from reamber.sm.SMMap import SMMap
from reamber.sm.lists.notes import SMHitList, SMHoldList, SMMineList, SMLiftList, SMRollList, SMFakeList, SMKeySoundList
from tests.test.sm.test_fixture import sm_mapset

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

MAP_WRITE_EXP = os.path.join(THIS_DIR, 'map_write_expected.sm')
MAP_WRITE = os.path.join(THIS_DIR, 'map_write.sm')

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

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

def test_mapset_loop(sm_mapset):
    for m in sm_mapset:
        assert isinstance(m, SMMap)

def test_counts(sm_mapset):
    assert len(sm_mapset[0].hits)  == 1816
    assert len(sm_mapset[0].holds) == 47
    assert len(sm_mapset[1].hits)  == 2512
    assert len(sm_mapset[1].holds) == 165

def test_write(sm_mapset):
    sm_mapset.write_file(MAP_WRITE)
    with open(MAP_WRITE_EXP) as f:
        expected = f.read()
    with open(MAP_WRITE) as f:
        actual = f.read()
    if expected != actual:
        assert False

def test_draw(sm_mapset):
    pf = PlayField(sm_mapset.maps[1], padding=50) \
         + PFDrawBeatLines() \
         + PFDrawNotes() \
         + PFDrawBpm()
    pf.export_fold(max_height=2300).save("sm.png")

def test_describe(sm_mapset):
    sm_mapset.describe()

def test_meta(sm_mapset):
    assert sm_mapset.title             == "Escapes"
    assert sm_mapset.subtitle          == "subtitle"
    assert sm_mapset.artist            == "Draw the Emotional x Foreground Eclipse"
    assert sm_mapset.title_translit    == "titletranslit"
    assert sm_mapset.subtitle_translit == "subtitletranslit"
    assert sm_mapset.artist_translit   == "artisttranslit"
    assert sm_mapset.genre             == "genre"
    assert sm_mapset.credit            == "credit"
    assert sm_mapset.banner            == "Escapes - bn.png"
    assert sm_mapset.background        == "Escapes - bg.jpg"
    assert sm_mapset.lyrics_path       == "lyricspath"
    assert sm_mapset.cd_title          == "CDTitle.gif"
    assert sm_mapset.music             == "Escapes.mp3"
    assert sm_mapset.offset            == -635
    assert sm_mapset.sample_start      == 68502
    assert sm_mapset.sample_length     == 26000
    assert sm_mapset.selectable

def test_deepcopy(sm_mapset):
    m = sm_mapset.deepcopy()
    assert m is not sm_mapset
    test_meta(m)

def test_rate(sm_mapset):
    sms = sm_mapset.rate(0.5)
    assert np.all(sm_mapset.stack.offset.min() * 2 == sms.stack.offset.min())

import os

import numpy as np

from reamber.o2jam.lists.notes.O2JHitList import O2JHitList
from reamber.o2jam.lists.notes.O2JHoldList import O2JHoldList
from tests.test.o2jam.test_fixture import o2j_mapset

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

MAP_WRITE_EXP = os.path.join(THIS_DIR, 'map_write_expected.sm')
MAP_WRITE = os.path.join(THIS_DIR, 'map_write.sm')

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *


# @profile
def test_type(o2j_mapset):
    assert isinstance(o2j_mapset[0].hits, O2JHitList)
    assert isinstance(o2j_mapset[0].holds, O2JHoldList)

def test_mapset_loop(o2j_mapset):
    for m in o2j_mapset:
        assert isinstance(m, O2JMap)

def test_counts(o2j_mapset):
    assert len(o2j_mapset[0].hits)  == 1816
    assert len(o2j_mapset[0].holds) == 47
    assert len(o2j_mapset[1].hits)  == 2512
    assert len(o2j_mapset[1].holds) == 165

def test_draw(o2j_mapset):
    pf = PlayField(o2j_mapset.maps[1], padding=0) \
         + PFDrawBeatLines() \
         + PFDrawNotes() \
         + PFDrawBpm()
    pf.export_fold(max_height=1200).save("o2j.png")

def test_describe(o2j_mapset):
    o2j_mapset.describe()

def test_meta(o2j_mapset):
    assert o2j_mapset.title             == "Escapes"
    assert o2j_mapset.subtitle          == "subtitle"
    assert o2j_mapset.artist            == "Draw the Emotional x Foreground Eclipse"
    assert o2j_mapset.title_translit    == "titletranslit"
    assert o2j_mapset.subtitle_translit == "subtitletranslit"
    assert o2j_mapset.artist_translit   == "artisttranslit"
    assert o2j_mapset.genre             == "genre"
    assert o2j_mapset.credit            == "credit"
    assert o2j_mapset.banner            == "Escapes - bn.png"
    assert o2j_mapset.background        == "Escapes - bg.jpg"
    assert o2j_mapset.lyrics_path       == "lyricspath"
    assert o2j_mapset.cd_title          == "CDTitle.gif"
    assert o2j_mapset.music             == "Escapes.mp3"
    assert o2j_mapset.offset            == -635
    assert o2j_mapset.sample_start      == 68502
    assert o2j_mapset.sample_length     == 26000
    assert o2j_mapset.selectable

def test_deepcopy(o2j_mapset):
    m = o2j_mapset.deepcopy()
    assert m is not o2j_mapset
    test_meta(m)

def test_rate(o2j_mapset):
    sms = o2j_mapset.rate(0.5)
    assert np.all(o2j_mapset.stack.offset.min() * 2 == sms.stack.offset.min())

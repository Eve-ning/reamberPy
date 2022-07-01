from pathlib import Path

import pytest

from reamber.sm.SMMapSet import SMMapSet


def test_read():
    with open(MAP_PATH) as f:
        content = f.readlines()


def test_write(sm_mapset):
    sm_mapset.write()


def test_meta(sm_mapset):
    sms = SMMapSet.read_file(MAP_PATH)
    assert sms.title == "Escapes"
    assert sms.subtitle == "subtitle"
    assert sms.artist == "Draw the Emotional x Foreground Eclipse"
    assert sms.title_translit == "titletranslit"
    assert sms.subtitle_translit == "subtitletranslit"
    assert sms.artist_translit == "artisttranslit"
    assert sms.genre == "genre"
    assert sms.credit == "credit"
    assert sms.banner == "Escapes - bn.png"
    assert sms.background == "Escapes - bg.jpg"
    assert sms.lyrics_path == "lyricspath"
    assert sms.cd_title == "CDTitle.gif"
    assert sms.music == "Escapes.mp3"
    assert sms.offset == -635
    assert sms.sample_start == 68502
    assert sms.sample_length == 26000
    assert sms.selectable

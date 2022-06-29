from pathlib import Path

from reamber.sm.SMMapSet import SMMapSet

MAP_PATH = Path(__file__).parent / "map.sm"


def test_counts(sm_mapset):
    assert len(sm_mapset[0].hits) == 1816
    assert len(sm_mapset[0].holds) == 47
    assert len(sm_mapset[1].hits) == 2512
    assert len(sm_mapset[1].holds) == 165


def test_write():
    with open(MAP_PATH) as f:
        content = f.readlines()
        m = SMMapSet.read(content)
        assert m.write() == "".join(content)


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

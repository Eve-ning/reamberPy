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
    assert sm_mapset.title == "Escapes"
    assert sm_mapset.subtitle == "subtitle"
    assert sm_mapset.artist == "Draw the Emotional x Foreground Eclipse"
    assert sm_mapset.title_translit == "titletranslit"
    assert sm_mapset.subtitle_translit == "subtitletranslit"
    assert sm_mapset.artist_translit == "artisttranslit"
    assert sm_mapset.genre == "genre"
    assert sm_mapset.credit == "credit"
    assert sm_mapset.banner == "Escapes - bn.png"
    assert sm_mapset.background == "Escapes - bg.jpg"
    assert sm_mapset.lyrics_path == "lyricspath"
    assert sm_mapset.cd_title == "CDTitle.gif"
    assert sm_mapset.music == "Escapes.mp3"
    assert sm_mapset.offset == -635
    assert sm_mapset.sample_start == 68502
    assert sm_mapset.sample_length == 26000
    assert sm_mapset.selectable

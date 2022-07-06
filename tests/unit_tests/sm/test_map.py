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
    assert sm_mapset.offset == 635
    assert sm_mapset.sample_start == 68502
    assert sm_mapset.sample_length == 26000
    assert sm_mapset.selectable

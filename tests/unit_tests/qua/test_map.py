from pathlib import Path

from reamber.quaver.QuaMapMeta import QuaMapMode

MAP_PATH = Path(__file__).parent / "map.qua"

from reamber.quaver import QuaMap


def test_type(qua_map):
    assert isinstance(qua_map, QuaMap)


def test_meta(qua_map):
    assert qua_map.audio_file == "audio.mp3"
    assert qua_map.song_preview_time == 169955
    assert qua_map.background_file == "bg.jpg"
    assert qua_map.banner_file == "banner.png"
    assert qua_map.genre == "genre"
    assert not qua_map.bpm_does_not_affect_scroll_velocity
    assert qua_map.initial_scroll_velocity == 1.0
    assert qua_map.has_scratch_key
    assert qua_map.map_id == -1
    assert qua_map.map_set_id == -1
    assert qua_map.mode == QuaMapMode.KEYS_7
    assert qua_map.title == "Carry Me Away (Extended Mix)"
    assert qua_map.artist == "lapix"
    assert qua_map.source == ''
    assert qua_map.tags == []
    assert qua_map.creator == "Evening"
    assert qua_map.difficulty_name == "Airbound (Evening's Flip)"
    assert qua_map.description == "This is a Quaver converted " \
                                  "version of Evening's map."
    assert qua_map.editor_layers == []
    assert qua_map.custom_audio_samples == []
    assert qua_map.sound_effects == []


def test_write():
    with open(MAP_PATH) as f:
        content = f.readlines()
        m = QuaMap.read(content)
        assert m.write() == "".join(content)

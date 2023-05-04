import os
from pathlib import Path

import pytest

from reamber.osu import OsuSampleSet as Sample, OsuMap
from reamber.osu.OsuMapMeta import OsuMapMode
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuSvList import OsuSvList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList

THIS_DIR = Path(__file__).parent

MAP_READ = THIS_DIR / 'map_read.osu'

m = OsuMap.read_file(MAP_READ)


def test_read_bad():
    with pytest.raises(Exception):
        OsuMap.read(["bad_string"])
    with pytest.raises(Exception):
        OsuMap.read([])


def test_types(osu_map):
    assert isinstance(osu_map.hits, OsuHitList)
    assert isinstance(osu_map.holds, OsuHoldList)
    assert isinstance(osu_map.svs, OsuSvList)
    assert isinstance(osu_map.bpms, OsuBpmList)
    assert isinstance(osu_map.objs, dict)


def test_write():
    with open(MAP_READ) as f:
        expected = f.read()

    assert expected == "\n".join(m.write())


def test_meta():
    assert "audio.mp3" == m.audio_file_name
    assert 0 == m.audio_lead_in
    assert 86398 == m.preview_time
    assert not m.countdown
    assert Sample.SOFT == m.sample_set
    assert 0.7 == m.stack_leniency
    assert OsuMapMode.MANIA == m.mode
    assert not m.letterbox_in_breaks
    assert not m.special_style
    assert m.widescreen_storyboard
    assert 0.4 == m.distance_spacing
    assert 8 == m.beat_divisor
    assert 4 == m.grid_size
    assert 1.9 == m.timeline_zoom
    assert "Tribal Trial" == m.title
    assert "Tribal Trial" == m.title_unicode
    assert "Yooh" == m.artist
    assert "Yooh" == m.artist_unicode
    assert "Tofu1222" == m.creator
    assert "Murumoo's EXHAUST" == m.version
    assert "SOUND VOLTEX VIVID WAVE" == m.source
    assert ["BEMANI", "KONAMI", "SDVX", "V", "5", "Murumoo", "Unpredictable",
            "FAMoss", "Video", "Game", "Instrumental"] == m.tags
    assert 2062527 == m.beatmap_id
    assert 965664 == m.beatmap_set_id
    assert 7.5 == m.hp_drain_rate
    assert 4 == m.circle_size
    assert 7.5 == m.overall_difficulty
    assert 5 == m.approach_rate
    assert 1.4 == m.slider_multiplier
    assert 1 == m.slider_tick_rate
    assert "BG.png" == m.background_file_name


def test_sample():
    assert m.samples[0].data.to_dict() == \
           dict(offset=24565, sample_file='"clap.wav"', volume=70)


def test_rate_noln():
    m = OsuMap.read_file(os.path.join(THIS_DIR, 'map_noln.osu'))
    assert m.stack().offset.min() * 2 == m.rate(0.5).stack().offset.min()

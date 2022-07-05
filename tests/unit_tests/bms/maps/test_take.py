from pathlib import Path

import pytest

from reamber.algorithms.convert import BMSToOsu
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import PFDrawBeatLines, PFDrawNotes, \
    PFDrawBpm
from reamber.bms.BMSChannel import BMSChannel
from reamber.bms.BMSMap import BMSMap
from tests.unit_tests.conftest import MAPS_DIR

THIS_DIR = Path(__file__).parent


@pytest.fixture()
def bms_map():
    return BMSMap.read_file(MAPS_DIR / "bms/take.bms",
                            BMSChannel.BME)


def test_first_hit(bms_map):
    assert bms_map.hits.first_offset() == pytest.approx(1200, abs=1)


def test_last_hit(bms_map):
    assert bms_map.hits.last_offset() == \
           pytest.approx(2 * 60000 + 11256, abs=2)


def test_bpms(bms_map):
    s = bms_map.stack()

    print(s[s.offset >=  29269].bpm)


def test_write(bms_map):
    osu = BMSToOsu.convert(bms_map)
    osu.stack().offset += 110
    osu.audio_file_name = "audio.mp3"
    osu.beatmap_set_id = 1376486
    osu.circle_size = 8
    osu.creator = "Evening"
    osu.version = "conv"
    osu.title = "Take"
    osu.artist = "Risshuu feat. Choko"
    osu.write_file(
        "D:/Program Files/osu!/Songs/1376486 Risshuu feat Choko - Take/Risshuu feat. Choko - Take (Evening) [conv].osu")


def test_draw(bms_map):
    # bms_map.write_file(MAP_WRITE)
    pf = PlayField(bms_map, padding=50) \
         + PFDrawBeatLines() \
         + PFDrawNotes() \
         + PFDrawBpm()
    pf.export_fold(max_height=2300).save("take.png")

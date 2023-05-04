from pathlib import Path

import pytest

from reamber.algorithms.convert import BMSToOsu
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import PFDrawBeatLines, PFDrawNotes, \
    PFDrawBpm
from reamber.bms.BMSMap import BMSMap
from tests.conftest import MAPS_DIR

THIS_DIR = Path(__file__).parent


@pytest.fixture()
def bms_map():
    return BMSMap.read_file(MAPS_DIR / "bms/nhelv.bme")


@pytest.mark.xfail(reason="Not supporting Nhelv.")
def test_last_offset_check(bms_map):
    # Rough check that this is correctly done
    assert bms_map.hits.last_offset() < 156000


@pytest.mark.skip("Not supporting Nhelv.")
def test_write(bms_map):
    osu = BMSToOsu.convert(bms_map)
    osu.audio_file_name = "audio.mp3"
    osu.circle_size = 8
    osu.version = 'test'
    osu.creator = 'Evening'

    osu.beatmap_set_id = 1344506
    osu.write_file("...")


@pytest.mark.skip("Not supporting Nhelv.")
def test_draw():
    bms = BMSMap.read_file(MAPS_DIR / "bms/nhelv.bme")
    pf = PlayField(bms, padding=50) \
         + PFDrawBeatLines() \
         + PFDrawNotes() \
         + PFDrawBpm()
    pf.export_fold(max_height=2300).save("nhelv.png")

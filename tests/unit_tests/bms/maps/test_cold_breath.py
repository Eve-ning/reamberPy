from pathlib import Path

import pytest

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import PFDrawBeatLines, PFDrawNotes, \
    PFDrawBpm
from reamber.bms.BMSMap import BMSMap
from tests.unit_tests.conftest import MAPS_DIR

THIS_DIR = Path(__file__).parent


@pytest.fixture()
def bms_map():
    return BMSMap.read_file(MAPS_DIR / "bms/coldBreath.bme")


def test_first_hit(bms_map):
    assert bms_map.hits.first_offset() == pytest.approx(1200, abs=1)


def test_last_hit(bms_map):
    assert bms_map.hits.last_offset() == \
           pytest.approx(2 * 60000 + 11256, abs=2)


def test_draw():
    bms = BMSMap.read_file(MAPS_DIR / "bms/coldBreath.bme")
    # bms_map.write_file(MAP_WRITE)
    pf = PlayField(bms, padding=50) \
         + PFDrawBeatLines() \
         + PFDrawNotes() \
         + PFDrawBpm()
    pf.export_fold(max_height=2300).save("bms.png")

def test_write(bms_map):
    bms_map.write_file("coldBreath.bme")
    # pf = PlayField(bms, padding=50) \
    #      + PFDrawBeatLines() \
    #      + PFDrawNotes() \
    #      + PFDrawBpm()
    # pf.export_fold(max_height=2300).save("bms.png")

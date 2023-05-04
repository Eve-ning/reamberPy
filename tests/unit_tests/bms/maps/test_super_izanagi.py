from pathlib import Path

import pytest

from reamber.bms.BMSChannel import BMSChannel
from reamber.bms.BMSMap import BMSMap
from tests.conftest import MAPS_DIR

THIS_DIR = Path(__file__).parent


@pytest.fixture()
def bms_map():
    return BMSMap.read_file(MAPS_DIR / "bms/superIzanagi.bme",
                            BMSChannel.BME)


def test_map(bms_map):
    with open(Path(__file__).parent / "gt_superIzanagi.bme", 'rb') as f:
        b = f.read()
    assert bms_map.write().splitlines() == b.splitlines()

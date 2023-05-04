from pathlib import Path

import pytest

from reamber.bms.BMSMap import BMSMap
from tests.conftest import MAPS_DIR

THIS_DIR = Path(__file__).parent


@pytest.fixture()
def bms_map():
    return BMSMap.read_file(MAPS_DIR / "bms/coldBreath.bme")


def test_map(bms_map):
    with open(Path(__file__).parent / "gt_coldBreath.bme", 'rb') as f:
        b = f.read()
    assert hash(bms_map.write()) == hash(b)

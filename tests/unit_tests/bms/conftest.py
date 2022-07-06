from pathlib import Path

import pytest

from reamber.bms import BMSMap

THIS_DIR = Path(__file__).parent

MAP_PATH = THIS_DIR / 'searoad.bml'


@pytest.fixture(scope='package')
def bms_map() -> BMSMap:
    return BMSMap.read_file(MAP_PATH)

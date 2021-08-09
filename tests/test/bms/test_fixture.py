import os

import pytest

from reamber.bms import BMSMap

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

MAP_READ = os.path.join(THIS_DIR, 'take.bms')


@pytest.fixture(scope='package')
def bms_map() -> BMSMap:
    return BMSMap.read_file(MAP_READ)

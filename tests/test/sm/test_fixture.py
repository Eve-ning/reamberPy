import os
import pytest

from reamber.sm import SMMapSet
from reamber.sm.SMMap import SMMap

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

MAP_READ = os.path.join(THIS_DIR, 'ICFITU.sm')

@pytest.fixture(scope='package')
def sm_mapset() -> SMMapSet:
    return SMMapSet.read_file(MAP_READ)


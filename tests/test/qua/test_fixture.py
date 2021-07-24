import os
import pytest

from reamber.quaver import QuaMap

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

MAP_READ = os.path.join(THIS_DIR, 'CarryMeAway.qua')

@pytest.fixture(scope='package')
def qua_map() -> QuaMap:
    return QuaMap.read_file(MAP_READ)

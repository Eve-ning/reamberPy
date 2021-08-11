import os
import pytest

from reamber.o2jam import O2JMapSet

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

MAP_READ = os.path.join(THIS_DIR, 'o2ma178.ojn')

@pytest.fixture(scope='package')
def o2j_mapset() -> O2JMapSet:
    return O2JMapSet.read_file(MAP_READ)

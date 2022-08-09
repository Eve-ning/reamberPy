from pathlib import Path

import numpy as np
import pytest

from reamber.bms.BMSMap import BMSMap
from reamber.o2jam import O2JMapSet
from reamber.osu import OsuMap
from reamber.quaver import QuaMap
from reamber.sm import SMMapSet

RSC_DIR = Path(__file__).parents[1] / 'rsc'
MAPS_DIR = RSC_DIR / 'maps'
REPS_OSU_DIR = RSC_DIR / 'reps/osu'


@pytest.fixture(scope='session')
def osu_map():
    return OsuMap.read_file((MAPS_DIR / 'osu/Gravity.osu').as_posix())


@pytest.fixture(scope='session')
def qua_map():
    return QuaMap.read_file((MAPS_DIR / 'qua/CarryMeAway.qua').as_posix())


@pytest.fixture(scope='session')
def sm_mapset():
    return SMMapSet.read_file((MAPS_DIR / 'sm/Escapes.sm').as_posix())


@pytest.fixture(scope='session')
def sm_map(sm_mapset):
    return sm_mapset[0]


@pytest.fixture(scope='session')
def o2j_mapset():
    return O2JMapSet.read_file((MAPS_DIR / 'o2jam/o2ma178.ojn').as_posix())


@pytest.fixture(scope='session')
def o2j_map(o2j_mapset):
    return o2j_mapset[0]


@pytest.fixture(scope='session')
def bms_map():
    return BMSMap.read_file(MAPS_DIR / 'bms/coldBreath.bme')


@pytest.fixture(scope='session')
def randintp():
    return 42


@pytest.fixture(scope='session')
def randintpm():
    return -42


@pytest.fixture(scope='session')
def rand():
    return np.random.rand()


@pytest.fixture
def columns():
    return np.array([0, 1, 2, 3])


@pytest.fixture
def offsets():
    return np.array([0, 100, 200, 300])


@pytest.fixture
def bpm_bpms():
    return np.asarray([300, 300, 200, 200])


@pytest.fixture
def bpm_metronomes():
    return np.asarray([4, 4, 3, 5])

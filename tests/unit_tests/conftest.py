from pathlib import Path

import pytest

from reamber.bms.BMSMap import BMSMap
from reamber.o2jam import O2JMapSet
from reamber.osu import OsuMap
from reamber.quaver import QuaMap
from reamber.sm import SMMapSet

RSC_DIR = Path(__file__).parents[2] / 'rsc/maps'


@pytest.fixture(scope='session')
def osu_map():
    return OsuMap.read_file((RSC_DIR / 'osu/Gravity.osu').as_posix())


@pytest.fixture(scope='session')
def qua_map():
    return QuaMap.read_file((RSC_DIR / 'qua/CarryMeAway.qua').as_posix())


@pytest.fixture(scope='session')
def sm_mapset():
    return SMMapSet.read_file((RSC_DIR / 'sm/Escapes.sm').as_posix())


@pytest.fixture(scope='session')
def sm_map():
    return sm_mapset[0]


@pytest.fixture(scope='session')
def o2j_mapset():
    return O2JMapSet.read_file((RSC_DIR / 'o2jam/o2ma178.ojn').as_posix())


@pytest.fixture(scope='session')
def o2j_map():
    return o2j_mapset[0]


@pytest.fixture(scope='session')
def bms_map():
    return BMSMap.read_file(RSC_DIR / 'bms/coldBreath.bme')

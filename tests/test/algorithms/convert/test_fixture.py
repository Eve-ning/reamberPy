import os
import pytest

from reamber.bms.BMSMap import BMSMap
from reamber.o2jam import O2JMapSet
from reamber.osu.OsuMap import OsuMap
from reamber.quaver.QuaMap import QuaMap
from reamber.sm import SMMapSet

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

OSU_READ = os.path.join(THIS_DIR, 'Gravity.osu')
QUA_READ = os.path.join(THIS_DIR, 'CarryMeAway.qua')
SM_READ = os.path.join(THIS_DIR, 'Escapes.sm')
O2J_READ = os.path.join(THIS_DIR, 'o2ma178.ojn')
BMS_READ = os.path.join(THIS_DIR, 'coldBreath.bme')

@pytest.fixture(scope='package')
def osu() -> OsuMap:
    return OsuMap.read_file(OSU_READ)

@pytest.fixture(scope='package')
def qua() -> QuaMap:
    return QuaMap.read_file(QUA_READ)

@pytest.fixture(scope='package')
def sms() -> SMMapSet:
    return SMMapSet.read_file(SM_READ)

@pytest.fixture(scope='package')
def o2js() -> O2JMapSet:
    return O2JMapSet.read_file(O2J_READ)

@pytest.fixture(scope='package')
def bms() -> BMSMap:
    return BMSMap.read_file(BMS_READ)

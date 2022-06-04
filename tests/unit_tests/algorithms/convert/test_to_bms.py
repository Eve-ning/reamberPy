import pytest

from reamber.algorithms.convert import O2JToBMS, OsuToBMS, QuaToBMS, SMToBMS
from reamber.bms.BMSChannel import BMSChannel


def test_o2j(o2j_mapset):
    bmss = O2JToBMS.convert(o2js)
    bmss[0].write(BMSChannel.BME)

def test_osu(osu):
    bms = OsuToBMS.convert(osu, move_right_by=1)
    bms.write(BMSChannel.BME)

def test_qua(qua):
    bms = QuaToBMS.convert(qua, move_right_by=1)
    bms.write(BMSChannel.BME)

def test_sm(sms):
    bmss = SMToBMS.convert(sms)
    bmss[0].write(BMSChannel.BME)


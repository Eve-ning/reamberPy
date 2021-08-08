from reamber.algorithms.convert import O2JToBMS, OsuToBMS, QuaToBMS, SMToBMS
from reamber.bms.BMSChannel import BMSChannel
from tests.test.algorithms.convert.test_fixture import o2js, osu, qua, bms, sms


def test_o2j(o2js):
    # Complex BPM Points
    bmss = O2JToBMS.convert(o2js)
    bmss[0].write_file('out.bme', BMSChannel.BME)

def test_osu(osu):
    # Complex BPM Points
    bms = OsuToBMS.convert(osu, move_right_by=1)
    bms.write_file('out.bme', BMSChannel.BME)

def test_qua(qua):
    # Complex BPM Points
    bms = QuaToBMS.convert(qua, move_right_by=1)
    bms.write_file('out.bme', BMSChannel.BME)

def test_sm(sms):
    bmss = SMToBMS.convert(sms)
    bmss[0].write_file('out.bme', BMSChannel.BME)


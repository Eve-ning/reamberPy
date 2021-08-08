from reamber.algorithms.convert import O2JToSM, OsuToSM, QuaToSM, BMSToSM
from tests.test.algorithms.convert.test_fixture import o2js, osu, qua, bms, sms


def test_o2j(o2js):
    smss = O2JToSM.convert(o2js)
    smss[0].write_file('out.sm')

def test_osu(osu):
    sms = OsuToSM.convert(osu)
    sms.write_file('out.sm')

def test_qua(qua):
    sms = QuaToSM.convert(qua)
    sms.write_file('out.sm')

def test_bms(bms):
    sms = BMSToSM.convert(bms)
    sms.write_file('out.sm')


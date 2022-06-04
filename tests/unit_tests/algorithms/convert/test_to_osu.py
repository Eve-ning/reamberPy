from reamber.algorithms.convert import O2JToOsu, BMSToOsu, QuaToOsu, SMToOsu
from tests.test.algorithms.convert.test_fixture import o2js, osu, qua, bms, sms


def test_o2j(o2js):
    osus = O2JToOsu.convert(o2js)
    osus[0].write_file('out.osu')

def test_osu(bms):
    osu = BMSToOsu.convert(bms)
    osu.write_file('out.osu')

def test_qua(qua):
    osu = QuaToOsu.convert(qua)
    osu.write_file('out.osu')

def test_sm(sms):
    osus = SMToOsu.convert(sms)
    osus[0].write_file('out.osu')


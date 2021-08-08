from reamber.algorithms.convert import O2JToOsu, BMSToOsu, QuaToOsu, SMToOsu
from tests.test.algorithms.convert.test_fixture import o2js, osu, qua, bms, sms


def test_o2j(o2js):
    # Complex BPM Points
    osus = O2JToOsu.convert(o2js)
    osus[0].write_file('out.osu')

def test_osu(bms):
    # Complex BPM Points
    osu = BMSToOsu.convert(bms)
    osu.write_file('out.osu')

def test_qua(qua):
    # Complex BPM Points
    osu = QuaToOsu.convert(qua)
    osu.write_file('out.osu')

def test_sm(sms):
    osus = SMToOsu.convert(sms)
    osus[0].write_file('out.osu')


from reamber.algorithms.convert import O2JToQua, OsuToQua, BMSToQua, SMToQua
from tests.test.algorithms.convert.test_fixture import o2js, osu, qua, bms, sms


def test_o2j(o2js):
    quas = O2JToQua.convert(o2js)
    quas[0].write_file('out.qua')

def test_osu(osu):
    qua = OsuToQua.convert(osu)
    qua.write_file('out.qua')

def test_qua(bms):
    qua = BMSToQua.convert(bms)
    qua.write_file('out.qua')

def test_sm(sms):
    quas = SMToQua.convert(sms)
    quas[0].write_file('out.qua')


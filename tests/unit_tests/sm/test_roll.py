import pandas as pd

from reamber.sm import SMRoll
from tests.test.sm.test_fixture import sm_mapset


# def test_type(sm_mapset):
#     assert isinstance(sm_mapset[0].rolls[0], SMRoll)

def test_from_series():
    roll = SMRoll.from_series(pd.Series(dict(offset=1000, column=1, length=1000)))
    assert SMRoll(1000, 1, 1000) == roll

import pandas as pd

from reamber.sm import SMFake
from tests.test.sm.test_fixture import sm_mapset


# def test_type(sm_mapset):
#     assert isinstance(sm_mapset[0].hits[0], SMFake)

def test_from_series():
    fake = SMFake.from_series(pd.Series(dict(offset=1000, column=1)))
    assert SMFake(1000, 1) == fake

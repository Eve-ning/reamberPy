import pandas as pd

from reamber.sm import SMLift
from tests.test.sm.test_fixture import sm_mapset


# def test_type(sm_mapset):
#     assert isinstance(sm_mapset[0].lifts[0], SMLift)

def test_from_series():
    lift = SMLift.from_series(pd.Series(dict(offset=1000, column=1)))
    assert SMLift(1000, 1) == lift

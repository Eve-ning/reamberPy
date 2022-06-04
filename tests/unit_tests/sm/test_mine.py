import pandas as pd

from reamber.sm import SMMine
from tests.test.sm.test_fixture import sm_mapset


# def test_type(sm_mapset):
#     assert isinstance(sm_mapset[0].hits[0], SMMine)

def test_from_series():
    mine = SMMine.from_series(pd.Series(dict(offset=1000, column=1)))
    assert SMMine(1000, 1) == mine

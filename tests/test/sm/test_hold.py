import pandas as pd

from reamber.sm import SMHold
from tests.test.sm.test_fixture import sm_mapset

def test_type(sm_mapset):
    assert isinstance(sm_mapset[0].holds[0], SMHold)

def test_from_series():
    hold = SMHold.from_series(pd.Series(dict(offset=1000, column=1, length=1000)))
    assert SMHold(1000, 1, 1000) == hold

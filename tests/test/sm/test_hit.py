import pandas as pd

from reamber.sm import SMHit
from tests.test.sm.test_fixture import sm_mapset


def test_type(sm_mapset):
    assert isinstance(sm_mapset[0].hits[0], SMHit)

def test_from_series():
    hit = SMHit.from_series(pd.Series(dict(offset=1000, column=1)))
    assert SMHit(1000, 1) == hit

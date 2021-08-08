import pandas as pd

from reamber.o2jam import O2JHit
from tests.test.o2jam.test_fixture import o2j_mapset


def test_type(o2j_mapset):
    assert isinstance(o2j_mapset[0].hits[0], O2JHit)

def test_from_series():
    hit = O2JHit.from_series(pd.Series(dict(offset=1000, column=1, volume=2, pan=3)))
    assert O2JHit(1000, 1, 2, 3) == hit

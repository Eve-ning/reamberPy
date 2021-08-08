import pandas as pd

from reamber.o2jam.O2JHold import O2JHold
from tests.test.o2jam.test_fixture import o2j_mapset


def test_type(o2j_mapset):
    assert isinstance(o2j_mapset[0].holds[0], O2JHold)

def test_from_series():
    hold = O2JHold.from_series(pd.Series(dict(offset=1000, column=1, length=1000, volume=2, pan=3)))
    assert O2JHold(1000, 1, 1000, 2, 3) == hold

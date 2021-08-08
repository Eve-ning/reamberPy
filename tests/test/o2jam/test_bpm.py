import pandas as pd

from reamber.o2jam import O2JBpm
from tests.test.o2jam.test_fixture import o2j_mapset


# @profile
def test_type(o2j_mapset):
    assert isinstance(o2j_mapset[0].bpms[0], O2JBpm)

def test_from_series():
    bpm = O2JBpm.from_series(pd.Series(dict(offset=1000, bpm=300, metronome=4)))
    assert bpm == O2JBpm(offset=1000, bpm=300)

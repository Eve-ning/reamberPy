import pandas as pd

from reamber.sm import SMBpm
from tests.test.sm.test_fixture import sm_mapset


# @profile
def test_type(sm_mapset):
    assert isinstance(sm_mapset[0].bpms[0], SMBpm)

def test_from_series():
    bpm = SMBpm.from_series(pd.Series(dict(offset=1000, bpm=300, metronome=4)))
    assert bpm == SMBpm(offset=1000, bpm=300)

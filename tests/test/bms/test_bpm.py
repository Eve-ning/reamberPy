import pandas as pd

from reamber.bms import BMSBpm
from tests.test.bms.test_fixture import bms_map


# @profile
def test_type(bms_map):
    assert isinstance(bms_map.bpms[0], BMSBpm)

def test_from_series(bms_map):
    bpm = BMSBpm.from_series(pd.Series(dict(offset=1000, bpm=300, metronome=4)))
    assert bpm == BMSBpm(offset=1000, bpm=300, metronome=4)

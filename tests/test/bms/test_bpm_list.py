import pandas as pd

from reamber.bms.lists import BMSBpmList
from tests.test.bms.test_fixture import bms_map


def test_type(bms_map):
    assert isinstance(bms_map.hits.df, pd.DataFrame)

def test_df_names(bms_map):
    assert {'offset', 'metronome', 'bpm'} == set(bms_map.bpms.df.columns)

def test_empty(bms_map):
    assert {'offset', 'metronome', 'bpm'} == set(BMSBpmList([]).df.columns)


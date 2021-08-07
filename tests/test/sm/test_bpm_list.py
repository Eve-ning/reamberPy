import pandas as pd

from reamber.sm.lists.SMBpmList import SMBpmList
from tests.test.sm.test_fixture import sm_mapset


def test_type(sm_mapset):
    assert isinstance(sm_mapset[0].bpms.df, pd.DataFrame)

def test_df_names(sm_mapset):
    assert {'offset', 'metronome', 'bpm'} == set(sm_mapset[0].bpms.df.columns)

def test_empty(sm_mapset):
    assert {'offset', 'metronome', 'bpm'} == set(SMBpmList([]).df.columns)

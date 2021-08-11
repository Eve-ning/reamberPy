import pandas as pd

from reamber.o2jam.lists.O2JBpmList import O2JBpmList
from tests.test.o2jam.test_fixture import o2j_mapset


def test_type(o2j_mapset):
    assert isinstance(o2j_mapset[0].bpms, O2JBpmList)
    assert isinstance(o2j_mapset[0].bpms.df, pd.DataFrame)

def test_df_names(o2j_mapset):
    assert {'offset', 'metronome', 'bpm'} == set(o2j_mapset[0].bpms.df.columns)

def test_empty(o2j_mapset):
    assert {'offset', 'metronome', 'bpm'} == set(O2JBpmList([]).df.columns)

import pandas as pd

from reamber.sm.lists.notes import SMFakeList
from tests.test.sm.test_fixture import sm_mapset


def test_type(sm_mapset):
    assert isinstance(sm_mapset[0].fakes, SMFakeList)
    assert isinstance(sm_mapset[0].fakes.df, pd.DataFrame)

def test_df_names(sm_mapset):
    assert {'offset', 'column'} == set(sm_mapset[0].fakes.df.columns)

def test_empty():
    assert {'offset', 'column'} == set(SMFakeList([]).df.columns)

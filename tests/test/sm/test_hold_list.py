import pandas as pd

from reamber.sm.lists.notes import SMHoldList
from tests.test.sm.test_fixture import sm_mapset


def test_type(sm_mapset):
    assert isinstance(sm_mapset[0].holds, SMHoldList)
    assert isinstance(sm_mapset[0].holds.df, pd.DataFrame)

def test_df_names(sm_mapset):
    assert {'offset', 'column', 'length'} == set(sm_mapset[0].holds.df.columns)

def test_empty():
    assert {'offset', 'column', 'length'} == set(SMHoldList([]).df.columns)

import pandas as pd

from reamber.sm.lists.notes import SMLiftList
from tests.test.sm.test_fixture import sm_mapset


def test_type(sm_mapset):
    assert isinstance(sm_mapset[0].lifts, SMLiftList)
    assert isinstance(sm_mapset[0].lifts.df, pd.DataFrame)

def test_df_names(sm_mapset):
    assert {'offset', 'column'} == set(sm_mapset[0].lifts.df.columns)

def test_empty():
    assert {'offset', 'column'} == set(SMLiftList([]).df.columns)

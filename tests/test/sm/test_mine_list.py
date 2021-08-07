import pandas as pd

from reamber.sm.lists.notes import SMMineList
from tests.test.sm.test_fixture import sm_mapset


def test_type(sm_mapset):
    assert isinstance(sm_mapset[0].mines, SMMineList)
    assert isinstance(sm_mapset[0].mines.df, pd.DataFrame)

def test_df_names(sm_mapset):
    assert {'offset', 'column'} == set(sm_mapset[0].mines.df.columns)

def test_empty():
    assert {'offset', 'column'} == set(SMMineList([]).df.columns)

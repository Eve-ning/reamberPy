import pandas as pd

from reamber.o2jam.lists.notes.O2JHitList import O2JHitList
from tests.test.o2jam.test_fixture import o2j_mapset


def test_type(o2j_mapset):
    assert isinstance(o2j_mapset[0].hits, O2JHitList)
    assert isinstance(o2j_mapset[0].hits.df, pd.DataFrame)

def test_df_names(o2j_mapset):
    assert {'offset', 'column', 'volume', 'pan'} == set(o2j_mapset[0].hits.df.columns)

def test_empty():
    assert {'offset', 'column', 'volume', 'pan'} == set(O2JHitList([]).df.columns)

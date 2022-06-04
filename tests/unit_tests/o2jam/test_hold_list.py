import pandas as pd

from reamber.o2jam.lists.notes.O2JHoldList import O2JHoldList
from tests.test.o2jam.test_fixture import o2j_mapset


def test_type(o2j_mapset):
    assert isinstance(o2j_mapset[0].holds, O2JHoldList)
    assert isinstance(o2j_mapset[0].holds.df, pd.DataFrame)

def test_df_names(o2j_mapset):
    assert {'offset', 'column', 'length', 'volume', 'pan'} == set(o2j_mapset[0].holds.df.columns)

def test_empty():
    assert {'offset', 'column', 'length', 'volume', 'pan'} == set(O2JHoldList([]).df.columns)

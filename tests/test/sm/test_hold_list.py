import unittest

import pandas as pd

from reamber.bms.lists.notes import BMSHitList, BMSHoldList
from tests.test.bms.test_fixture import bms_map

def test_type(bms_map):
    assert isinstance(bms_map.holds.df, pd.DataFrame)

def test_df_names(bms_map):
    assert {'offset', 'column', 'length', 'sample'} == set(bms_map.holds.df.columns)

def test_empty(bms_map):
    assert {'offset', 'column', 'length', 'sample'} == set(BMSHoldList([]).df.columns)

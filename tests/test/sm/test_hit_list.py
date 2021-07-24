import unittest

import pandas as pd

from reamber.bms.lists.notes import BMSHitList
from tests.test.bms.test_fixture import bms_map

def test_type(bms_map):
    assert isinstance(bms_map.hits.df, pd.DataFrame)

def test_df_names(bms_map):
    assert {'offset', 'column', 'sample'} == set(bms_map.hits.df.columns)

def test_empty(bms_map):
    assert {'offset', 'column', 'sample'} == set(BMSHitList([]).df.columns)


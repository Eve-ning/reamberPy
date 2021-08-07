import pandas as pd

from reamber.bms import BMSHit
from tests.test.bms.test_fixture import bms_map


def test_type(bms_map):
    assert isinstance(bms_map.hits[0], BMSHit)

def test_from_series():
    hit = BMSHit.from_series(pd.Series(dict(offset=1000, column=1, sample=b'0')))
    assert BMSHit(1000, 1, b'0') == hit


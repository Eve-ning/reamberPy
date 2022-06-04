import pandas as pd

from reamber.bms import BMSHold
from tests.test.bms.test_fixture import bms_map


def test_type(bms_map):
    assert isinstance(bms_map.holds[0], BMSHold)

def test_from_series():
    hold = BMSHold.from_series(pd.Series(dict(offset=1000, column=1, length=1000, sample=b'0')))
    assert BMSHold(1000, 1, 1000, b'0') == hold

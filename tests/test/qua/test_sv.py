import unittest

import pandas as pd

from reamber.quaver import QuaBpm, QuaSv
from tests.test.qua.test_fixture import qua_map

def test_type(qua_map):
    assert isinstance(qua_map.bpms[0], QuaBpm)

def test_from_series():
    sv = QuaSv.from_series(pd.Series(dict(offset=1000, multiplier=2.0)))
    assert QuaSv(offset=1000, multiplier=2.0) == sv

def test_from_yaml_dict():
    sv = QuaSv.from_yaml_dict(dict(StartTime=1000, Multiplier=2.0))
    assert sv == QuaSv(offset=1000, multiplier=2.0)
    return sv

def test_to_yaml_dict():
    assert test_from_yaml_dict().to_yaml_dict() == dict(StartTime=1000, Multiplier=2.0)



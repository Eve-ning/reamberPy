import pandas as pd

from reamber.quaver import QuaHold
from tests.test.qua.test_fixture import qua_map

def test_type(qua_map):
    assert isinstance(qua_map.holds[0], QuaHold)

def test_from_series():
    hit = QuaHold.from_series(
        pd.Series(dict(offset=1000, column=1, keysounds=['a.wav', 'b.wav'], length=1000))
    )
    assert QuaHold(offset=1000, column=1, keysounds=['a.wav', 'b.wav'], length=1000) == hit

def test_from_yaml_dict():
    obj = QuaHold.from_yaml_dict(dict(StartTime=1000, Lane=1, KeySounds=['a.wav', 'b.wav'], EndTime=2000))
    assert obj == QuaHold(offset=1000, column=0, keysounds=['a.wav', 'b.wav'], length=1000)
    return obj

def test_to_yaml_dict():
    assert test_from_yaml_dict().to_yaml_dict() == \
           dict(StartTime=1000, Lane=1, KeySounds=['a.wav', 'b.wav'], EndTime=2000)

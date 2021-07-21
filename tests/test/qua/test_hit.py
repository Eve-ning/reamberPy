import pandas as pd

from reamber.quaver import QuaHit


def test_type(qua_map):
    assert isinstance(qua_map.hits[0], QuaHit)

def test_from_series():
    hit = QuaHit.from_series(
        pd.Series(dict(offset=1000, column=1, keysounds=['a.wav', 'b.wav']))
    )
    assert QuaHit(offset=1000, column=1, keysounds=['a.wav', 'b.wav']) == hit

def test_from_yaml_dict():
    obj = QuaHit.from_yaml_dict(dict(StartTime=1000, Lane=1, KeySounds=['a.wav', 'b.wav']))
    assert obj == QuaHit(offset=1000, column=0, keysounds=['a.wav', 'b.wav'])
    return obj

def test_to_yaml_dict():
    assert test_from_yaml_dict().to_yaml_dict() == dict(StartTime=1000, Lane=1, KeySounds=['a.wav', 'b.wav'])


import unittest

import pandas as pd

from reamber.quaver import QuaBpm
from tests.test.qua.test_fixture import qua_map

def test_type(qua_map):
    assert isinstance(qua_map.bpms[0], QuaBpm)

def test_from_series():
    bpm = QuaBpm.from_series(pd.Series(dict(offset=1000, bpm=100, metronome=4)))
    assert QuaBpm(offset=1000, bpm=100, metronome=4) == bpm

def test_from_yaml_dict():
    bpm = QuaBpm.from_yaml_dict(dict(StartTime=1000, Bpm=100))
    assert bpm == QuaBpm(offset=1000, bpm=100, metronome=4)
    return bpm

def test_to_yaml_dict():
    assert test_from_yaml_dict().to_yaml_dict() == dict(StartTime=1000, Bpm=100)



import pandas as pd

from reamber.quaver.lists.QuaBpmList import QuaBpmList
from tests.test.qua.test_fixture import qua_map


def test_type(qua_map):
    assert isinstance(qua_map.bpms, QuaBpmList)

def test_df_names(qua_map):
    assert {'offset', 'bpm', 'metronome'}, set(qua_map.bpms.df.columns)

def test_to_yaml(qua_map):
    assert set(qua_map.bpms.to_yaml()[0].keys()) == {'StartTime', 'Bpm'}


from reamber.quaver.lists.notes import QuaHoldList
from tests.test.qua.test_fixture import qua_map


def test_type(qua_map):
    assert isinstance(qua_map.holds, QuaHoldList)

def test_df_names(qua_map):
    assert {'offset', 'column', 'length', 'key_sounds'}, set(qua_map.holds.df.columns)

def test_to_yaml(qua_map):
    assert set(qua_map.holds.to_yaml()[0].keys()) == {'StartTime', 'Lane', 'KeySounds', 'EndTime'}


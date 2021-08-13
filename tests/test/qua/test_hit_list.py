from reamber.quaver.lists.notes import QuaHitList
from tests.test.qua.test_fixture import qua_map


def test_type(qua_map):
    assert isinstance(qua_map.hits, QuaHitList)

def test_df_names(qua_map):
    assert {'offset', 'column', 'keysounds'}, set(qua_map.hits.df.columns)

def test_to_yaml(qua_map):
    assert set(qua_map.hits.to_yaml()[0].keys()) == {'StartTime', 'Lane', 'KeySounds'}


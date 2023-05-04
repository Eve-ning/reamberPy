def test_df_names(qua_map):
    assert {'offset', 'bpm', 'metronome'} == set(qua_map.bpms.df.columns)


def test_to_yaml(qua_map):
    assert set(qua_map.bpms.to_yaml()[0].keys()) == {'StartTime', 'Bpm'}

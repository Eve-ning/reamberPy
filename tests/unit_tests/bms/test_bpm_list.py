from reamber.bms.lists import BMSBpmList


def test_df_names(bms_map):
    assert {'offset', 'metronome', 'bpm'} == set(bms_map.bpms.df.columns)


def test_empty(bms_map):
    assert {'offset', 'metronome', 'bpm'} == set(BMSBpmList([]).df.columns)

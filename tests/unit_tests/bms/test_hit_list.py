from reamber.bms.lists.notes import BMSHitList


def test_df_names(bms_map):
    assert {'offset', 'column', 'sample'} == set(bms_map.hits.df.columns)


def test_empty(bms_map):
    assert {'offset', 'column', 'sample'} == set(BMSHitList([]).df.columns)

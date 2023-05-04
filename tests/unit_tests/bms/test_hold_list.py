from reamber.bms.lists.notes import BMSHoldList


def test_df_names(bms_map):
    assert {'offset', 'column', 'length', 'sample'} == set(
        bms_map.holds.df.columns)


def test_empty(bms_map):
    assert {'offset', 'column', 'length', 'sample'} == set(
        BMSHoldList([]).df.columns)

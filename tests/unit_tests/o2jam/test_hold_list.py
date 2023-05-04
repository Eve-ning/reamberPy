from reamber.o2jam.lists.notes.O2JHoldList import O2JHoldList


def test_df_names(o2j_mapset):
    assert {'offset', 'column', 'length', 'volume', 'pan'} == set(
        o2j_mapset[0].holds.df.columns)


def test_empty():
    assert {'offset', 'column', 'length', 'volume', 'pan'} == set(
        O2JHoldList([]).df.columns)

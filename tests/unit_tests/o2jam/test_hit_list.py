from reamber.o2jam.lists.notes.O2JHitList import O2JHitList


def test_df_names(o2j_mapset):
    assert {'offset', 'column', 'volume', 'pan'} == set(
        o2j_mapset[0].hits.df.columns)


def test_empty():
    assert {'offset', 'column', 'volume', 'pan'} == set(
        O2JHitList([]).df.columns)

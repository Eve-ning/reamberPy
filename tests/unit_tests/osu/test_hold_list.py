from reamber.osu import OsuSampleSet as Sample
from reamber.osu.lists.notes import OsuHoldList

S0 = Sample.AUTO
S1 = Sample.NORMAL
S2 = Sample.SOFT
S3 = Sample.DRUM


def test_df_names(hold_list):
    assert {'offset', 'column', 'length', 'hitsound_set', 'sample_set',
            'addition_set', 'custom_set', 'volume', 'hitsound_file'} == \
           set(hold_list.df.columns)


def test_read(hold_strings, columns, offsets):
    holds = OsuHoldList.read(hold_strings, keys=4)
    assert (columns == holds.column.to_list()).all()
    assert (offsets == holds.offset.to_list()).all()


def test_write(hold_strings):
    holds = OsuHoldList.read(hold_strings, keys=4)
    assert hold_strings == holds.write(4)


def test_empty():
    assert {'offset', 'column', 'length', 'hitsound_set', 'sample_set',
         'addition_set', 'custom_set', 'volume', 'hitsound_file'} == \
        set(OsuHoldList([]).df.columns)

from reamber.osu import OsuSampleSet as Sample
from reamber.osu.lists.notes import OsuHitList

S0 = Sample.AUTO
S1 = Sample.NORMAL
S2 = Sample.SOFT
S3 = Sample.DRUM


def test_df_names(hit_list):
    assert ['offset', 'column', 'hitsound_set', 'sample_set',
            'addition_set', 'custom_set', 'volume', 'hitsound_file'] \
           == list(hit_list.df.columns)


def test_samples(hit_list: OsuHitList):
    assert [S0, S1, S2, S3] == hit_list.sample_set.to_list()
    assert [S0, S1, S2, S3] == hit_list.addition_set.to_list()
    assert [S0, S1, S2, S3] == hit_list.hitsound_set.to_list()
    assert [S0, S1, S2, S3] == hit_list.custom_set.to_list()


def test_read_editor_string(offsets, columns):
    hits = OsuHitList.read_editor_string(
        "00:00:100 (0|0, 100|1, 200|2, 300|3) -"
    )
    assert (columns == hits.column.to_list()).all()
    assert (offsets == hits.offset.to_list()).all()


def test_read(hit_strings, offsets, columns):
    hits = OsuHitList.read(hit_strings, keys=4)
    assert (columns == hits.column.to_list()).all()
    assert (offsets == hits.offset.to_list()).all()


def test_write(hit_strings):
    hits = OsuHitList.read(hit_strings, keys=4)
    assert hit_strings == hits.write(4)


def test_empty():
    assert {'offset', 'column', 'hitsound_set', 'sample_set', 'addition_set',
            'custom_set', 'volume', 'hitsound_file'} == \
           set(OsuHitList([]).df.columns)

from reamber.osu import OsuSampleSet as Sample
from reamber.osu.lists import OsuBpmList

S0 = Sample.AUTO
S1 = Sample.NORMAL
S2 = Sample.SOFT
S3 = Sample.DRUM


def test_df_names(bpm_list):
    assert set(bpm_list.df.columns) == \
           {'offset', 'bpm', 'metronome', 'sample_set', 'sample_set_index',
            'volume', 'kiai'}


def test_read(bpm_strings, bpm_bpms, offsets):
    bpms = OsuBpmList.read(bpm_strings)
    assert all(bpm_bpms == bpms.bpm.to_list())
    assert all(offsets == bpms.offset.to_list())


def test_write(bpm_list, bpm_strings):
    assert bpm_strings == bpm_list.write()

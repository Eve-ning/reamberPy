import pytest

from reamber.osu import OsuBpm, OsuSampleSet as Sample


def test_meta(bpm):
    assert Sample.DRUM == bpm.sample_set
    assert 1 == bpm.sample_set_index
    assert 10 == bpm.volume
    assert bpm.kiai


def test_code_to_value():
    assert [200, 300, 100] == [OsuBpm.code_to_value(v) for v in
                               [300, 200, 600]]
    assert [200, 300, 100] == [OsuBpm.value_to_code(v) for v in
                               [300, 200, 600]]


def test_read(bpm_string, bpm):
    bpm_ = OsuBpm.read_string(bpm_string)
    assert bpm, bpm_
    bpm_ = OsuBpm.read_string("2000,300,5,3,1,10,1,0")
    assert OsuBpm(offset=2000, bpm=200, metronome=5, sample_set=Sample.DRUM,
                  sample_set_index=1,
                  volume=10, kiai=False) == bpm_


def test_read_bad():
    with pytest.raises(ValueError):
        OsuBpm.read_string("bad_string")
    with pytest.raises(ValueError):
        OsuBpm.read_string("")


def test_read_bad_sv():
    with pytest.raises(ValueError):
        OsuBpm.read_string("1000,-200,4,2,1,30,0,0")


def test_read_inf():
    with pytest.raises(ZeroDivisionError):
        OsuBpm.read_string("1000,0,4,2,1,30,1,0")


def test_write(bpm_string):
    assert bpm_string == OsuBpm.read_string(bpm_string).write_string()


def test_is_timing_point():
    assert OsuBpm.is_timing_point("1000,200,4,3,1,10,1,1")
    assert not OsuBpm.is_timing_point("1000,200,4,3,1,10,0,1")

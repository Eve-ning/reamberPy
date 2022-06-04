import pandas as pd
import pytest

from reamber.base.lists import BpmList


def test_type(bpm_list):
    assert isinstance(bpm_list.df, pd.DataFrame)


def test_bpms(bpm_list):
    assert [300, 300, 200, 200] == bpm_list.bpm.to_list()


def test_bpms_change(bpm_list):
    bpm_list.bpm *= 2
    assert [600, 600, 400, 400] == bpm_list.bpm.to_list()


def test_metronome(bpm_list):
    assert [4, 4, 3, 5] == bpm_list.metronome.to_list()


def test_metronome_change(bpm_list):
    bpm_list.metronome += 1
    assert [5, 5, 4, 6] == bpm_list.metronome.to_list()


def test_init_single_and_multiple(bpms):
    """ Tests whether initializing with a single item list is different from a single item """
    assert BpmList(bpms[0:1]) == BpmList(bpms[0])


def test_ix_slice(bpm_list, bpms):
    a = bpm_list[0:2]
    assert isinstance(a, BpmList)
    assert 2 == len(a)
    assert BpmList(bpms[0:2]) == a


def test_ix_bool(bpm_list):
    a = bpm_list[bpm_list.metronome != 4]
    assert isinstance(a, BpmList)
    assert 2 == len(a)
    assert 1600 == a[0].offset
    assert 2500 == a[1].offset
    assert 3 == a[0].metronome
    assert 5 == a[1].metronome


def test_empty_handling(bpm_list):
    # Check if empty initialization works
    # noinspection PyTypeChecker

    assert (BpmList([]).bpm == bpm_list.between(500, 750).bpm).all
    # Check if truly empty
    assert BpmList([]).df.empty
    assert bpm_list.between(500, 750).df.empty


def test_to_timing_map(bpm_list):
    bpm_list.to_timing_map()


def test_ave_bpm(bpm_list):
    assert 250 == bpm_list.ave_bpm(3200)


def test_current_bpm(bpm_list):
    assert 800 == bpm_list.current_bpm(900).offset
    assert 800 == bpm_list.current_bpm(800).offset
    assert 800 == bpm_list.current_bpm(799.999).offset
    with pytest.raises(IndexError):
        bpm_list.current_bpm(-1)

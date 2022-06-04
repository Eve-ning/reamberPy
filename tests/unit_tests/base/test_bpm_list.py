import pandas as pd
import pytest

from reamber.base.lists import BpmList


def test_type(bpm_list):
    assert isinstance(bpm_list.df, pd.DataFrame)


def test_bpms(bpm_list, bpm_bpms):
    assert bpm_bpms == bpm_list.bpm.to_list()


def test_bpms_change(bpm_list, bpm_bpms):
    bpm_list.bpm *= 2
    assert bpm_bpms * 2 == bpm_list.bpm.to_list()


def test_metronome(bpm_list, bpm_metronomes):
    assert bpm_metronomes == bpm_list.metronome.to_list()


def test_metronome_change(bpm_list, bpm_metronomes):
    bpm_list.metronome += 1
    assert bpm_metronomes == bpm_list.metronome.to_list()


def test_init_single_and_multiple(bpms):
    assert BpmList(bpms[0:1]) == BpmList(bpms[0])


def test_ix_slice(bpm_list, bpms):
    a = bpm_list[0:2]
    assert isinstance(a, BpmList)
    assert 2 == len(a)
    assert BpmList(bpms[0:2]) == a


def test_ix_bool(bpm_list, bpm_offsets, bpm_metronomes):
    a = bpm_list[bpm_list.metronome != 4]
    assert isinstance(a, BpmList)
    assert 2 == len(a)
    assert bpm_offsets[2] == a[0].offset
    assert bpm_offsets[3] == a[1].offset
    assert bpm_metronomes[2] == a[0].metronome
    assert bpm_metronomes[3] == a[1].metronome


def test_empty_handling(bpm_list):

    assert (BpmList([]).bpm == bpm_list.between(500, 750).bpm).all
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

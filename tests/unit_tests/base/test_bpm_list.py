import numpy as np
import pytest


def test_to_timing_map(bpm_list):
    bpm_list.to_timing_map()


def test_ave_bpm(bpm_list, offsets, bpm_bpms):
    last_offset = offsets[-1] + 100
    first_offset = offsets[0]
    ave_bpm = np.sum(np.diff(offsets, append=last_offset) * bpm_bpms) / \
              (last_offset - first_offset)
    assert ave_bpm == bpm_list.ave_bpm(last_offset)


def test_current_bpm(bpm_list, offsets, bpm_bpms):
    assert bpm_bpms[0] == bpm_list.current_bpm(offsets[0]).bpm
    assert bpm_bpms[0] == bpm_list.current_bpm(offsets[1] - 1).bpm
    assert bpm_bpms[1] == bpm_list.current_bpm(offsets[1]).bpm
    with pytest.raises(IndexError):
        bpm_list.current_bpm(offsets[0] - 1)

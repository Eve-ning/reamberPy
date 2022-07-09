import numpy as np
import pytest

from reamber.osu import OsuBpm, OsuSampleSet as Sample, OsuHit, OsuHold, OsuSv
from reamber.osu.lists import OsuBpmList, OsuSvList
from reamber.osu.lists.notes import OsuHitList, OsuHoldList
# noinspection PyUnresolvedReferences
from tests.unit_tests.base.conftest import hold_lengths


S0 = Sample.AUTO
S1 = Sample.NORMAL
S2 = Sample.SOFT
S3 = Sample.DRUM


@pytest.fixture
def sv_muls():
    return np.array([1, 2, 0.5, 4])


@pytest.fixture
def bpm_strings(offsets, bpm_bpms, bpm_metronomes, hitsound_sets, volumes):
    return [
        f"{offset},{OsuBpm.code_to_value(bpm)},"
        f"{metronome},{hitsound_set},0,{volume},1,1"
        for offset, bpm, metronome, hitsound_set, volume in
        zip(offsets, bpm_bpms, bpm_metronomes, hitsound_sets,
            volumes)
    ]


@pytest.fixture
def sv_strings(offsets, sv_muls, hitsound_sets, volumes):
    return [
        f"{offset},{OsuSv.code_to_value(sv)},"
        f"4,{hitsound_set},0,{volume},0,1"
        for offset, sv, hitsound_set, volume in
        zip(offsets, sv_muls, hitsound_sets, volumes)
    ]


@pytest.fixture
def hit_strings(offsets, columns, hitsound_sets, volumes):
    keys = np.max(columns) + 1
    return [
        f"{OsuHit.column_to_x_axis(column, keys)},192,{offset},1,"
        f"{hitsound_set},"
        f"{hitsound_set}:{hitsound_set}:{hitsound_set}:{volume}:"
        for offset, column, hitsound_set, volume in
        zip(offsets, columns, hitsound_sets, volumes)
    ]


@pytest.fixture
def hold_strings(offsets, columns, hold_lengths, hitsound_sets, volumes):
    keys = np.max(columns) + 1
    return [
        f"{OsuHold.column_to_x_axis(column, keys)},192,{offset},128,"
        f"{hitsound_set},{hold_length}:"
        f"{hitsound_set}:{hitsound_set}:{hitsound_set}:{volume}:"
        for offset, column, hold_length, hitsound_set, volume in
        zip(offsets, columns, hold_lengths, hitsound_sets, volumes)
    ]


@pytest.fixture
def bpm_list(offsets, bpm_bpms, bpm_metronomes, hitsound_sets, volumes):
    return OsuBpmList([
        OsuBpm(offset, bpm, metronome, hitsound_set, 0, volume, True)
        for offset, bpm, metronome, hitsound_set, volume in
        zip(offsets, bpm_bpms, bpm_metronomes, hitsound_sets,
            volumes)
    ])


@pytest.fixture
def sv_list(offsets, sv_muls, hitsound_sets, volumes):
    return OsuSvList([
        OsuSv(offset, sv, 4, hitsound_set, 0, volume, True)
        for offset, sv, hitsound_set, volume in
        zip(offsets, sv_muls, hitsound_sets, volumes)
    ])


@pytest.fixture
def hit_list(offsets, columns, bpm_metronomes, hitsound_sets, volumes):
    return OsuHitList([
        OsuHit(offset, column, hitsound_set, hitsound_set, hitsound_set,
               hitsound_set, volume, "")
        for offset, column, hitsound_set, volume in
        zip(offsets, columns, hitsound_sets, volumes)
    ])


@pytest.fixture
def hold_list(offsets, columns, hold_lengths, bpm_metronomes, hitsound_sets,
              volumes):
    return OsuHoldList([
        OsuHold(offset, column, hold_length, hitsound_set, hitsound_set,
                hitsound_set, hitsound_set, volume, "")
        for offset, column, hold_length, hitsound_set, volume in
        zip(offsets, columns, hold_lengths, hitsound_sets, volumes)
    ])


@pytest.fixture
def volumes():
    return np.array([10, 20, 30, 40])


@pytest.fixture
def hitsound_sets():
    return np.array([S0, S1, S2, S3])


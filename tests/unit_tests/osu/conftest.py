import numpy as np
import pytest

from reamber.osu import OsuBpm, OsuSampleSet as Sample
from reamber.osu.lists import OsuBpmList

S0 = Sample.AUTO
S1 = Sample.NORMAL
S2 = Sample.SOFT
S3 = Sample.DRUM


@pytest.fixture
def bpm_strings(offsets, bpm_bpms, bpm_metronomes, hitsound_sets, volumes):
    return [
        f"{offset},{OsuBpm.code_to_value(bpm)}," \
        f"{metronome},{hitsound_set},0,{volume},1,1"
        for offset, bpm, metronome, hitsound_set, volume in
        zip(offsets, bpm_bpms, bpm_metronomes, hitsound_sets,
            volumes)
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
def volumes():
    return np.array([10, 20, 30, 40])


@pytest.fixture
def hitsound_sets():
    return np.array([S0, S1, S2, S3])

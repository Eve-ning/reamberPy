import pytest

from reamber.algorithms.generate.sv.SvSequence import SvSequence
from reamber.osu.OsuMap import OsuMap
from reamber.osu.OsuSv import OsuSv
from tests.unit_tests.RSC_PATHS import OSU_CARAVAN


def test_sv_io():
    # Complex BPM Points
    osu = OsuMap.read_file(OSU_CARAVAN)

    seq = SvSequence()
    seq.read_sv_from_map(osu)

    for sv, sv0 in zip(seq.write_as_sv(OsuSv, volume=0)[:50], osu.svs):
        assert isinstance(sv, OsuSv)
        assert sv0.multiplier == pytest.approx(sv.multiplier)


def test_true_sv_io():
    # Complex BPM Points
    osu = OsuMap.read_file(OSU_CARAVAN)

    seq = SvSequence()
    seq.read_true_sv_from_map(osu, 140)

    # Just need to check the first 50, others should be ok.
    for sv in seq.write_as_sv(OsuSv, volume=0)[:50]:
        assert isinstance(sv, OsuSv)
        assert sv.multiplier == pytest.approx(1, abs=0.01)

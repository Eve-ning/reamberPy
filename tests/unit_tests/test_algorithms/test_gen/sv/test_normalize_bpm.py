import pytest

from reamber.algorithms.generate.sv.generators.svNormalizeBpm import \
    sv_normalize_bpm
from reamber.base.Bpm import Bpm
from reamber.base.lists.BpmList import BpmList


def test_normalize():
    seq = sv_normalize_bpm(
        BpmList([Bpm(0, 200), Bpm(100, 50), Bpm(300, 100)]), 100
    )
    assert seq[0].multiplier == pytest.approx(0.5)
    assert seq[1].multiplier == pytest.approx(2.0)
    assert seq[2].multiplier == pytest.approx(1.0)

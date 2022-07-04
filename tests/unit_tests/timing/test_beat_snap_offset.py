import pytest

from reamber.algorithms.timing.TimingMap import TimingMap
from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.Snapper import Snapper
from reamber.algorithms.timing.utils.snap import Snap

tm = TimingMap.from_bpm_changes_offset([BpmChangeOffset(60000, 4, 0)])
snapper = Snapper()


@pytest.mark.parametrize(
    "offsets",
    [
        [0, 1, 2],
        [0, 1, 0],
        [2, 1, 0],
        [0, 0, 0],
        [1, 1, 1],
    ]
)
def test_beats(offsets):
    tm = TimingMap.from_bpm_changes_offset([BpmChangeOffset(60000, 4, 0)])
    assert offsets == list(tm.beats(offsets, snapper))


@pytest.mark.parametrize(
    "offsets",
    [
        [0, 1, 2],
        [0, 1, 0],
        [2, 1, 0],
        [0, 0, 0],
        [1, 1, 1],
    ]
)
def test_snaps(offsets):
    assert [Snap(0, b, 4) for b in offsets] == list(tm.snaps(offsets, snapper))


@pytest.mark.parametrize(
    "snaps_beat",
    [
        [0, 1, 2],
        [0, 1, 0],
        [2, 1, 0],
        [0, 0, 0],
        [1, 1, 1],
    ]
)
def test_offsets(snaps_beat):
    snaps = [Snap(0, b, 4) for b in snaps_beat]
    assert snaps_beat == list(tm.offsets(snaps))

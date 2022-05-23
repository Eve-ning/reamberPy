from typing import List

from reamber.algorithms.timing.TimingMap import TimingMap
from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap

C = 60000


def scenario_tester(
    bpm_changes_offset: List[BpmChangeOffset],
    bpm_changes_snap: List[BpmChangeSnap]
):
    tm = TimingMap.from_bpm_changes_snap(0, bpm_changes_snap)
    assert tm.bpm_changes_offset == bpm_changes_offset
    tm = TimingMap.from_bpm_changes_offset(bpm_changes_offset)
    tm = TimingMap.from_bpm_changes_snap(0, tm.bpm_changes_snap)
    assert tm.bpm_changes_offset == bpm_changes_offset
    pass
    # assert tm_snap.bpm_changes_offset == bpm_changes_offset
    # assert tm_offset.bpm_changes == bpm_changes


def test_1(scenario_1):
    scenario_tester(scenario_1[0], scenario_1[1])
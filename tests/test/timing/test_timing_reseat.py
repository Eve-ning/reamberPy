from typing import List

from reamber.algorithms.timing.TimingMap import TimingMap
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap


def reseat(bpm_changes_snap: List[BpmChangeSnap],
           bpm_changes_snap_reseat: List[BpmChangeSnap]):
    assert bpm_changes_snap_reseat == \
           TimingMap.reseat_bpm_changes_snap(bpm_changes_snap)


def test_1(scenario_1_snap, scenario_1_snap_reseat):
    reseat(scenario_1_snap, scenario_1_snap_reseat)

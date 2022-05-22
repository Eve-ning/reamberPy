from __future__ import annotations

from typing import List

from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap


def from_bpm_changes_snap(initial_offset: float,
                          bpm_changes_snap: List[BpmChangeSnap]) -> 'TimingMap':
    """ Creates Timing Map from bpm changes in snaps

    Notes:
        1st BPM Change MUST be on Measure, Beat, Slot 0.
    """
    from reamber.algorithms.timing.TimingMap import TimingMap
    bpm_changes_snap.sort(key=lambda x: x.snap)

    assert bpm_changes_snap[0].snap.measure == 0 and \
           bpm_changes_snap[0].snap.beat == 0 and \
           bpm_changes_snap[0].snap.division == 0, \
        f"The first bpm must be on Measure 0, Beat 0, Division 0. "
    bpm_changes_offset = [
        BpmChangeOffset(bpm_changes_snap[0].bpm,
                        bpm_changes_snap[0].metronome,
                        initial_offset)
    ]

    offset = initial_offset
    active_bpm_change = bpm_changes_snap[0]

    for bpm_change in bpm_changes_snap[1:]:
        offset += (bpm_change.snap - active_bpm_change.snap) \
            .offset(active_bpm_change)
        bpm_changes_offset.append(
            BpmChangeOffset(active_bpm_change.bpm,
                            active_bpm_change.metronome,
                            offset)
        )

    tm = TimingMap(initial_offset=initial_offset,
                   bpm_changes_offset=bpm_changes_offset)
    return tm

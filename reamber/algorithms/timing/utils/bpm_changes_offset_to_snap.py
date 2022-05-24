from __future__ import annotations

from typing import List

from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.Snapper import Snapper
from reamber.algorithms.timing.utils.snap import Snap


def bpm_changes_offset_to_snap(bpm_changes_offset: List[BpmChangeOffset],
                               snapper: Snapper) -> List[BpmChangeSnap]:
    """ Creates Timing Map from bpm changes in offset """
    bpm_changes_offset.sort(key=lambda x: x.offset)
    prev_bpm_change = bpm_changes_offset[0]

    prev_snap = Snap(0, 0, prev_bpm_change.metronome)
    bpm_changes_snap: List[BpmChangeSnap] = [
        BpmChangeSnap(bpm_changes_offset[0].bpm,
                      bpm_changes_offset[0].metronome,
                      snap=prev_snap)
    ]
    for bpm_change_offset in bpm_changes_offset[1:]:
        diff_offset = bpm_change_offset.offset - prev_bpm_change.offset

        snap = prev_snap + Snap.from_offset(diff_offset, prev_bpm_change,
                                            snapper)
        bpm_changes_snap.append(
            BpmChangeSnap(
                bpm=bpm_change_offset.bpm,
                metronome=bpm_change_offset.metronome,
                snap=snap
            )
        )
        prev_snap = snap
        prev_bpm_change = bpm_change_offset

    return bpm_changes_snap

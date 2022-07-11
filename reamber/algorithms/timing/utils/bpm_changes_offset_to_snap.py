from __future__ import annotations

from typing import List

from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.Snapper import Snapper
from reamber.algorithms.timing.utils.snap import Snap


def bpm_changes_offset_to_snap(bco_s: List[BpmChangeOffset],
                               snapper: Snapper) -> List[BpmChangeSnap]:
    """Creates Timing Map from bpm changes in offset

    Args:
        bco_s: BpmChange as Offsets to convert
        snapper: Snapping helper to snap offsets.
    """
    bco_s.sort(key=lambda x: x.offset)
    parent_bco = bco_s[0]

    prev_snap = Snap(0, 0, parent_bco.metronome)
    bcs_s: List[BpmChangeSnap] = [
        BpmChangeSnap(bco_s[0].bpm,
                      bco_s[0].metronome,
                      snap=prev_snap)
    ]
    for parent_bco, child_bco in zip(bco_s[:-1], bco_s[1:]):
        snap = Snap.from_offset(child_bco.offset,
                                parent_bco,
                                bcs_s[-1],
                                snapper)
        snap.metronome = child_bco.metronome
        bcs_s.append(
            BpmChangeSnap(
                bpm=child_bco.bpm,
                metronome=child_bco.metronome,
                snap=snap
            )
        )

    return bcs_s

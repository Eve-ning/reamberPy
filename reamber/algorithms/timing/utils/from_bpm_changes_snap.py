from __future__ import annotations

import logging
from copy import deepcopy
from typing import List

from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.reseat_bpm_changes_snap import \
    reseat_bpm_changes_snap


def from_bpm_changes_snap(initial_offset: float, bcs_s: List[BpmChangeSnap],
                          reseat: bool = True):
    """Creates Timing Map from bpm changes in snaps

    Notes:
        1st BPM Change MUST be on Measure, Beat, Slot 0.
    """
    bcs_s = deepcopy(bcs_s)
    from reamber.algorithms.timing.TimingMap import TimingMap
    bcs_s.sort(key=lambda x: x.snap)

    if bcs_s[0].snap.measure != 0 or bcs_s[0].snap.beat != 0:
        raise ValueError(f"The first bpm must be on Measure 0, Beat 0")

    bco_s = [BpmChangeOffset(bcs_s[0].bpm, bcs_s[0].metronome, initial_offset)]

    offset = initial_offset

    if reseat and any([bcs.snap.beat != 0 for bcs in bcs_s]):
        logging.warning("All Bpm Points must be on measures. Reseating")
        return from_bpm_changes_snap(
            initial_offset,
            reseat_bpm_changes_snap(bcs_s)
        )

    for parent_bcs, child_bcs in zip(bcs_s[:-1],
                                     bcs_s[1:]):
        diff_snap = child_bcs.snap - parent_bcs.snap

        offset += diff_snap.offset(parent_bcs)
        bco_s.append(
            BpmChangeOffset(child_bcs.bpm,
                            child_bcs.metronome,
                            offset)
        )

    tm = TimingMap(bpm_changes_offset=bco_s)
    return tm

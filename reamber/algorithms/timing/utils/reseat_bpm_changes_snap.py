from __future__ import annotations

from typing import List

from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.snap import Snap


def reseat_bpm_changes_snap(bcs_s: List[BpmChangeSnap]) -> List[BpmChangeSnap]:
    """ Force all bpm changes to be on metronome

    Notes:
        1st BPM Change MUST be on Measure, Beat, Slot 0.
    """
    bcs_s.sort(key=lambda x: x.snap)

    assert bcs_s[0].snap.measure == 0 and \
           bcs_s[0].snap.beat == 0, \
        f"The first bpm must be on Measure 0, Beat 0."

    new_bcs = [bcs_s[-1]]
    for ix in reversed(range(len(bcs_s) - 1)):
        parent_bc = bcs_s[ix]
        child_bc = bcs_s[ix + 1]

        diff_snap = child_bc.snap - parent_bc.snap

        # If it yields a perfect measure, we add and continue
        if diff_snap.beat == 0:
            new_bcs.insert(0, parent_bc)
            continue

        # Check if they are of the same measure, see below for usage.
        same_measure = child_bc.snap.measure == parent_bc.snap.measure

        # If round up increases by a measure, we move everything after
        if child_bc.snap.beat > 0:
            for b in new_bcs[1:]:
                b.snap.measure += 1
            child_bc.snap.round_up()

        new_bpm = parent_bc.bpm / (diff_snap.beat / parent_bc.metronome)

        if same_measure:
            # If in the same measure, we don't add a point
            new_bcs.insert(0,
                           BpmChangeSnap(new_bpm,
                                         parent_bc.metronome,
                                         parent_bc.snap)
                           )
        else:
            new_bcs.insert(0,
                           BpmChangeSnap(
                               new_bpm,
                               parent_bc.metronome,
                               Snap(child_bc.snap.measure - 1, 0,
                                    parent_bc.metronome))
                           )
            new_bcs.insert(0, parent_bc)

    return new_bcs

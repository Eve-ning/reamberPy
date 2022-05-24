from __future__ import annotations

from copy import deepcopy
from typing import List

from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap


def reseat_bpm_changes_snap(
    bpm_changes_snap: List[BpmChangeSnap]
) -> List[BpmChangeSnap]:
    """ Force all bpm changes to be on metronome

    Notes:
        1st BPM Change MUST be on Measure, Beat, Slot 0.
    """
    bpm_changes_snap.sort(key=lambda x: x.snap)

    assert bpm_changes_snap[0].snap.measure == 0 and \
           bpm_changes_snap[0].snap.beat == 0 and \
           f"The first bpm must be on Measure 0, Beat 0."
    new_bpm_changes_snap = [bpm_changes_snap[0]]
    for ix in range(len(bpm_changes_snap) - 1):
        active_bpm_change = bpm_changes_snap[ix]
        bpm_change = bpm_changes_snap[ix + 1]

        diff_snap = bpm_change.snap - active_bpm_change.snap
        # Find the difference with uneven measures
        if diff_snap.beat == 0:
            new_bpm_changes_snap.append(bpm_change)
            continue

        if diff_snap.measure == 0:
            # If the difference.measure == 0, replace previous bpm
            new_bpm_changes_snap.pop()

        for b in bpm_changes_snap[ix+1:]:
            # Push all future bpm_changes back
            b.snap += diff_snap

        correction = diff_snap.beat / active_bpm_change.metronome

        # Inject force-corrected bpm
        new_bpm = active_bpm_change.bpm / correction
        new_bpm_changes_snap.append(
            BpmChangeSnap(new_bpm,
                          active_bpm_change.metronome,
                          active_bpm_change.snap)
        )

        # Insert current bpm
        new_bpm_changes_snap.append(
            BpmChangeSnap(bpm_change.bpm,
                          bpm_change.metronome,
                          bpm_change.snap)
        )

    return new_bpm_changes_snap

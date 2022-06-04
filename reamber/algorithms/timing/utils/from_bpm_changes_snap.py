from __future__ import annotations

import logging
from typing import List

from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.reseat_bpm_changes_snap import \
    reseat_bpm_changes_snap


def from_bpm_changes_snap(initial_offset: float,
                          bpm_changes_snap: List[
                              BpmChangeSnap]) -> 'TimingMap':
    """ Creates Timing Map from bpm changes in snaps

    Notes:
        1st BPM Change MUST be on Measure, Beat, Slot 0.
    """
    from reamber.algorithms.timing.TimingMap import TimingMap
    bpm_changes_snap.sort(key=lambda x: x.snap)

    assert bpm_changes_snap[0].snap.measure == 0 and \
           bpm_changes_snap[0].snap.beat == 0 and \
           f"The first bpm must be on Measure 0, Beat 0"
    bpm_changes_offset = [
        BpmChangeOffset(bpm_changes_snap[0].bpm,
                        bpm_changes_snap[0].metronome,
                        initial_offset)
    ]

    offset = initial_offset

    for active_bpm_change, bpm_change in zip(bpm_changes_snap[:-1],
                                             bpm_changes_snap[1:]):
        diff_snap = bpm_change.snap - active_bpm_change.snap
        if diff_snap.beat != 0:
            logging.warning("All Bpm Points must be on measures. Reseating")
            return from_bpm_changes_snap(
                initial_offset,
                reseat_bpm_changes_snap(bpm_changes_snap)
            )

        offset += diff_snap.offset(active_bpm_change)
        bpm_changes_offset.append(
            BpmChangeOffset(bpm_change.bpm,
                            bpm_change.metronome,
                            offset)
        )

    tm = TimingMap(initial_offset=initial_offset,
                   bpm_changes_offset=bpm_changes_offset)
    return tm

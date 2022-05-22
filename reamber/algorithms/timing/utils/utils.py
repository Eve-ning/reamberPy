from __future__ import annotations

from typing import List

import numpy as np

from reamber.algorithms.timing import TimingMap
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset



def find_lcm(a: List, threshold: int) -> list:
    """ Find the LCM of each value lower than the threshold

    Examples:
        Take 4 numbers (1, 2, 3, 7), we find their respective LCM lower than n

        n | 15 | 9 | 5 |   n = 9 prevents 15 from forming
        --+----+---+---+
        1 | 15 | 6 | 2 |
        2 | 15 | 6 | 2 |
        3 | 15 | 6 | 3 |
        5 | 15 | 5 | 5 |

    Returns:
        Dict of input (key) and LCM (value)

    Args:
        a: List to reduce
        threshold: Highest value of LCM (exclusive)
    """
    a_ = [0 for _ in a]
    length = len(a)
    for i in range(length):
        for j in range(length):
            if i == j: continue
            b, c = a[i], a[j]
            if b is None or c is None: continue
            lcm = np.lcm(b, c)
            if lcm < threshold:
                a[i] = lcm
                a_[j] = lcm
                a[j] = None

    for i in range(length):
        if a_[i] == 0:
            a_[i] = a[i]

    return a_


def time_by_offset(bpm_changes_offset: List[BpmChangeOffset]) -> TimingMap:
    """ Creates Timing Map from bpm changes in offset """
    bpm_changes_offset.sort(key=lambda x: x.offset)
    initial_offset = bpm_changes_offset[0].offset
    for b in bpm_changes_offset:
        b.offset -= initial_offset
    return TimingMap(initial_offset=initial_offset,
                     bpm_changes_offset=bpm_changes_offset)


def time_by_snap(initial_offset: float,
                 bpm_changes_snap: List[BpmChangeSnap]) -> TimingMap:
    """ Creates Timing Map from bpm changes in snaps

    Notes:
        1st BPM Change MUST be on Measure, Beat, Slot 0.
    """
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

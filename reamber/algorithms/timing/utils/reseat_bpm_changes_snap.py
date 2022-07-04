from __future__ import annotations

from copy import deepcopy
from typing import List

from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.snap import Snap

THRES = 0


def reseat_bpm_changes_snap(bcs_s: List[BpmChangeSnap]) -> List[BpmChangeSnap]:
    """ Force all bpm changes to be on metronome

    Notes:
        1st BPM Change MUST be on Measure, Beat, Slot 0.
    """
    bcs_s = deepcopy(bcs_s)
    bcs_s.sort(key=lambda x: x.snap)

    offset = 0
    offsets = [0]
    for bcs_0, bcs_1 in zip(bcs_s[:-1], bcs_s[1:]):
        diff = (bcs_1.snap - bcs_0.snap).offset(bcs_0)
        offset += diff
        offsets.append(offset)

    i = 0
    measure = 0

    while i != len(bcs_s) - 1:
        bcs_0, bcs_1 = bcs_s[i], bcs_s[i + 1]
        offset_0, offset_1 = offsets[i], offsets[i + 1]
        offset_diff = offset_1 - offset_0
        measure_diff = offset_diff / bcs_0.measure_length
        measure_diff_quo = measure_diff // 1
        measure_diff_rem = measure_diff % 1
        measure += measure_diff_quo

        # BCS_0 is guaranteed to be on a measure.
        if measure_diff_rem > THRES:
            bcs = BpmChangeSnap(bcs_0.bpm / measure_diff_rem,
                                bcs_0.metronome,
                                Snap(measure, 0, bcs_0.metronome))
            offset = measure_diff_quo * bcs_0.measure_length + offset_0
            if measure_diff_quo == 0:
                bcs_s[i] = bcs
                offsets[i] = offset
                measure += 1
            else:
                bcs_s.insert(i + 1, bcs)
                offsets.insert(i + 1, offset)

        bcs_s[i + 1].snap.measure = measure
        bcs_s[i + 1].snap.beat = 0
        i += 1
    return bcs_s

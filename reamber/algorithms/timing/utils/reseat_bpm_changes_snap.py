from __future__ import annotations

from copy import deepcopy
from typing import List

from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.snap import Snap


def reseat_bpm_changes_snap(
    bcs_s: List[BpmChangeSnap],
    extend_threshold: float = 0.001
) -> List[BpmChangeSnap]:
    """Force all bpm changes to be on metronome

    Notes:
        The case where extend is used.
        BPM 60000, Offset 0     , Metronome 4
        BPM 60000, Offset 4.0001, Metronome 4

        Instead of adding a BPM on Offset 4, we simply change the first BPM.
        This prevents the case of a super high bpm.

    Args:
        bcs_s: Bpm Changes to reseat
        extend_threshold: Fraction of Measure to accept extending a late BPM

    Notes:
        1st BPM Change MUST be on Measure, Beat, Slot 0.
    """
    bcs_s = deepcopy(bcs_s)
    bcs_s.sort(key=lambda x: x.snap)

    offset = 0
    offsets = [0, ]
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
        beat_diff = offset_diff / bcs_0.beat_length
        beat_diff_quo = beat_diff // 1
        beat_diff_rem = beat_diff % 1
        measure_diff_quo = measure_diff // 1
        measure_diff_rem = measure_diff % 1
        measure += measure_diff_quo

        # BCS_0 is guaranteed to be on a measure.
        # Extend case, see docstring
        if 0 < measure_diff_rem <= extend_threshold:
            # Extend by nudging bpm
            bcs = BpmChangeSnap(bcs_0.bpm / (measure_diff_rem + 1),
                                bcs_0.metronome,
                                Snap(measure - 1, 0, bcs_0.metronome))
            offset = (measure_diff_quo - 1) * bcs_0.measure_length + offset_0
            if measure_diff_quo == 1:
                bcs_s[i] = bcs
                offsets[i] = offset
            else:
                measure -= 1
                bcs_s.insert(i + 1, bcs)
                offsets.insert(i + 1, offset)

        # Extend case, see docstring
        elif 0 < beat_diff_rem <= extend_threshold:
            # Check if it's possible to extend by changing metronome
            metronome = beat_diff_quo % bcs_0.metronome
            bcs = BpmChangeSnap(
                bcs_0.bpm / ((beat_diff_rem + metronome) / metronome),
                metronome,
                Snap(measure, 0, metronome)
            )
            offset = offset_1 - metronome * bcs_0.beat_length

            if measure_diff_quo == 0:
                # Modify prev bpm
                bcs_s[i] = bcs
                offsets[i] = offset
                measure += 1
            else:
                bcs_s.insert(i + 1, bcs)
                offsets.insert(i + 1, offset)

        elif measure_diff_rem > extend_threshold:
            # This means it's not possible to simply extend
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

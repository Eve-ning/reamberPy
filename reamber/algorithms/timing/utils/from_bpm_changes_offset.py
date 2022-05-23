from __future__ import annotations

from typing import List, TYPE_CHECKING

from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset


def from_bpm_changes_offset(
    bpm_changes_offset: List[BpmChangeOffset]
) -> 'TimingMap':
    from reamber.algorithms.timing.TimingMap import TimingMap
    """ Creates Timing Map from bpm changes in offset """
    bpm_changes_offset.sort(key=lambda x: x.offset)
    initial_offset = bpm_changes_offset[0].offset
    for b in bpm_changes_offset:
        b.offset -= initial_offset
    return TimingMap(initial_offset=initial_offset,
                     bpm_changes_offset=bpm_changes_offset)

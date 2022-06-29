from __future__ import annotations

from typing import List

from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset


def from_bpm_changes_offset(bco_s: List[BpmChangeOffset]) -> 'TimingMap':
    """ Creates TimingMap from bpm changes in offset """
    from reamber.algorithms.timing.TimingMap import TimingMap
    bco_s.sort(key=lambda x: x.offset)
    initial_offset = bco_s[0].offset
    for b in bco_s:
        b.offset -= initial_offset
    return TimingMap(initial_offset=initial_offset,
                     bpm_changes_offset=bco_s)

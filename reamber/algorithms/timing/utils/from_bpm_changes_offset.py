from __future__ import annotations

from typing import List

from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset


def from_bpm_changes_offset(bco_s: List[BpmChangeOffset]):
    """Creates TimingMap from bpm changes in offset"""
    from reamber.algorithms.timing.TimingMap import TimingMap
    bco_s.sort(key=lambda x: x.offset)
    return TimingMap(bpm_changes_offset=bco_s)

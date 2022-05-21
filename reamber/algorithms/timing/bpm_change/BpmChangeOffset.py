from __future__ import annotations

from dataclasses import dataclass

from reamber.algorithms.timing.bpm_change import BpmChangeBase


@dataclass
class BpmChangeOffset(BpmChangeBase):
    offset: float

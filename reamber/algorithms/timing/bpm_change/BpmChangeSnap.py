from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from reamber.algorithms.timing.bpm_change import BpmChangeBase
from reamber.base.RAConst import RAConst


@dataclass
class BpmChangeSnap(BpmChangeBase):
    measure: int
    beat: int
    slot: Fraction | float

    @property
    def beat_length(self) -> float:
        return RAConst.MIN_TO_MSEC / self.bpm

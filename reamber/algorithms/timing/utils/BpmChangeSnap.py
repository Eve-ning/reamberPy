from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from reamber.algorithms.timing.utils import BpmChangeBase
from reamber.base.RAConst import RAConst


@dataclass
class BpmChangeSnap(BpmChangeBase):
    measure: int
    beat: int
    snap: Fraction | float

    @property
    def beat_length(self) -> float:
        return RAConst.MIN_TO_MSEC / self.bpm

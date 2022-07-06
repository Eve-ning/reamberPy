from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from fractions import Fraction

from reamber.base.RAConst import RAConst


@dataclass
class BpmChangeBase(ABC):
    bpm: float
    metronome: Fraction | float

    @property
    def beat_length(self) -> float:
        return RAConst.MIN_TO_MSEC / self.bpm

    @property
    def measure_length(self) -> float:
        return self.beat_length * self.metronome

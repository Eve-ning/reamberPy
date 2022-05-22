from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import total_ordering

from reamber.algorithms.timing.utils.BpmChangeBase import BpmChangeBase
from reamber.algorithms.timing.utils.Snapper import Snapper




@total_ordering
@dataclass
class Snap:
    measure: int
    beat: int
    division: Fraction | float

    def __eq__(self, other: Snap):
        return (
            self.measure == other.measure and
            self.beat == other.beat and
            self.division == other.division
        )

    def __lt__(self, other: Snap):
        return (
            self.measure < other.measure and
            self.beat < other.beat and
            self.division < other.division
        )

    def __sub__(self, other: Snap):
        return Snap(
            self.measure - other.measure,
            self.beat - other.beat,
            self.division - other.division,
        )

    def __add__(self, other: Snap):
        return Snap(
            self.measure + other.measure,
            self.beat + other.beat,
            self.division + other.division,
        )

    def offset(self, bpm_active: BpmChangeBase):
        return (
            bpm_active.measure_length * self.measure +
            bpm_active.beat_length * (self.beat + self.division)
        )

    @staticmethod
    def from_offset(
        offset: float,
        bpm_active: BpmChangeBase,
        snapper: Snapper) -> Snap:
        measure = offset // bpm_active.measure_length
        offset -= measure * bpm_active.measure_length

        beat = offset // bpm_active.beat_length
        offset -= beat * bpm_active.beat_length

        division = snapper.snap(offset / bpm_active.beat_length)

        return Snap(measure, beat, division)

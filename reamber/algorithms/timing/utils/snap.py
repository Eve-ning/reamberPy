from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import total_ordering
from typing import TYPE_CHECKING

from reamber.algorithms.timing.utils.BpmChangeBase import BpmChangeBase
from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.Snapper import Snapper

if TYPE_CHECKING:
    from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap


@total_ordering
@dataclass(unsafe_hash=True)
class Snap:
    measure: int
    beat: Fraction | float
    # If metronome is none, don't correct anything
    metronome: Fraction | float | None

    def __post_init__(self):
        if self.metronome is None: return
        if self.measure < 0:
            self.beat += self.measure * self.metronome
        if (self.beat < 0) or (self.beat >= self.metronome):
            self.measure += self.beat // self.metronome
            self.beat %= Fraction(self.metronome)

        if (self.beat < 0) or (self.measure < 0):
            raise ValueError("Failed to yield positive Snap")

        self.beat = Fraction(self.beat)

    def __eq__(self, other: Snap):
        return self.measure == other.measure and self.beat == other.beat

    def __lt__(self, other: Snap):
        return self.measure < other.measure or \
               (self.measure == other.measure and self.beat < other.beat)

    def __sub__(self, other: Snap):
        return Snap(
            self.measure - other.measure,
            self.beat - other.beat,
            other.metronome
        )

    def __add__(self, other: Snap):
        return Snap(
            self.measure + other.measure,
            self.beat + other.beat,
            self.metronome
        )

    def offset(self, bpm_active: BpmChangeBase):
        return (
            bpm_active.measure_length * self.measure +
            bpm_active.beat_length * self.beat
        )

    @staticmethod
    def from_offset(offset: float,
                    bco: BpmChangeOffset,
                    bcs: BpmChangeSnap,
                    snapper: Snapper) -> Snap:
        """Calculate Snap from offset

        Args:
            offset: Offset to calculate from
            bco: The current active BpmChangeOffset
            bcs: The current active BpmChangeSnap
            snapper: Snapper helper instance
        """
        offset_del = offset - bco.offset
        measure = int(offset_del // bco.measure_length)
        offset_del -= measure * bco.measure_length
        beat = snapper.snap(offset_del / bco.beat_length)
        return Snap(measure + bcs.snap.measure,
                    beat + bcs.snap.beat, bco.metronome)

    def __repr__(self):
        return f"{self.measure}.{self.beat} / {self.metronome}"

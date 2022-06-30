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
    beat: Fraction | float
    metronome: Fraction | float

    def __post_init__(self):
        if self.measure < 0:
            self.beat += self.measure * self.metronome
        if (self.beat < 0) or (self.beat >= self.metronome):
            self.measure += self.beat // self.metronome
            self.beat %= Fraction(self.metronome)

        if (self.beat < 0) or (self.measure < 0):
            raise ValueError("Failed to yield positive Snap")

        self.beat = Fraction(self.beat)

    def __eq__(self, other: Snap):
        return (self.measure == other.measure and self.beat == other.beat)

    def __lt__(self, other: Snap):
        return self.measure < other.measure or \
               (self.measure == other.measure and self.beat < other.beat)

    def __sub__(self, other: Snap):
        return Snap(
            self.measure - other.measure,
            self.beat - other.beat,
            self.metronome
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
                    bpm_active: BpmChangeBase,
                    snapper: Snapper) -> Snap:
        """ Calculate Snap from offset

        Args:
            offset: Offset to calculate from
            bpm_active: The current BpmChange active
            snapper: Snapper helper instance
        """
        measure = int(offset // bpm_active.measure_length)
        offset -= measure * bpm_active.measure_length

        beat = snapper.snap(offset / bpm_active.beat_length)
        return Snap(measure, beat, bpm_active.metronome)

    def round_up(self):
        """ Rounds up the current snap inplace. """
        if self.beat > 0:
            self.measure += 1
            self.beat = 0


# %%
measure = 6
beat0 = 3
beat1 = 13 / 4
v = measure < measure or (measure == measure and beat0 < beat1)

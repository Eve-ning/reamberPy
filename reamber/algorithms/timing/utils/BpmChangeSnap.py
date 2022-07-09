from __future__ import annotations

from dataclasses import dataclass

from reamber.algorithms.timing.utils.BpmChangeBase import BpmChangeBase
from reamber.algorithms.timing.utils.snap import Snap


@dataclass
class BpmChangeSnap(BpmChangeBase):
    snap: Snap

    def __post_init__(self):
        if self.metronome != self.snap.metronome:
            raise Exception("Unexpected Error: Metronomes do not match.")

    def __repr__(self):
        return f"{self.bpm} BPM / {self.metronome} @ {self.snap}"

from src.base.TimedObject import TimedObject as TimedObject
from src.base.RAConst import RAConst
from dataclasses import dataclass


@dataclass
class TimingPoint(TimedObject):
    bpm: float = 120.0
    metronome: int = 4

    def beatLength(self) -> float:
        return RAConst.minToMSec(1.0 / self.bpm)

    def metronomeLength(self) -> float:
        return self.beatLength() * self.metronome


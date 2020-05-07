from __future__ import annotations
from src.osu.OsuTimingPointMeta import OsuTimingPointMeta
from src.base.TimingPoint import TimingPoint
from dataclasses import dataclass


@dataclass
class OsuTimingPoint(OsuTimingPointMeta, TimingPoint):
    @staticmethod
    def codeToValue(code: float) -> float:
        return 60000.0 / code

    @staticmethod
    def valueToCode(value: float) -> float:
        return 60000.0 / value

    @staticmethod
    def readString(s: str) -> OsuTimingPoint:
        if s.isspace():
            return None

        sComma = s.split(",")
        if len(sComma) < 8:
            return None

        this = OsuTimingPoint()
        this.offset = float(sComma[0])
        this.bpm = OsuTimingPoint.codeToValue(float(sComma[1]))
        this.metronome = int(sComma[2])
        this.sampleSet = int(sComma[3])
        this.sampleSetIndex = int(sComma[4])
        this.volume = int(sComma[5])
        this.kiai = int(sComma[7])

        return this

    def writeString(self) -> str:
        return f"{int(self.offset)},{self.valueToCode(self.bpm)}," \
               f"{self.metronome},{self.sampleSet}," \
               f"{self.sampleSetIndex},{self.volume},{1},{self.kiai}"

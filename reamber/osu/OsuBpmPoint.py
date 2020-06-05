from __future__ import annotations
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta
from reamber.base.BpmPoint import BpmPoint
from dataclasses import dataclass


@dataclass
class OsuBpmPoint(OsuTimingPointMeta, BpmPoint):
    @staticmethod
    def codeToValue(code: float) -> float:
        return 60000.0 / code

    @staticmethod
    def valueToCode(value: float) -> float:
        return 60000.0 / value

    @staticmethod
    def readString(s: str) -> OsuBpmPoint or None:
        if s.isspace(): return None

        sComma = s.split(",")
        if len(sComma) < 8: return None

        this = OsuBpmPoint()
        this.offset = float(sComma[0])
        this.bpm = OsuBpmPoint.codeToValue(float(sComma[1]))
        this.metronome = int(sComma[2])
        this.sampleSet = int(sComma[3])
        this.sampleSetIndex = int(sComma[4])
        this.volume = int(sComma[5])
        this.kiai = int(sComma[7])

        return this

    def writeString(self) -> str:
        return f"{int(self.offset)},{self.valueToCode(self.bpm)}," \
               f"{self.metronome},{self.sampleSet}," \
               f"{self.sampleSetIndex},{self.volume},{1},{int(self.kiai)}"

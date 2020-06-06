from __future__ import annotations
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta
from reamber.base.TimedObj import TimedObj
from dataclasses import dataclass


@dataclass
class OsuSvObj(OsuTimingPointMeta, TimedObj):
    multiplier: float = 1.0

    @staticmethod
    def codeToValue(code: float) -> float:
        return -100.0 / code

    @staticmethod
    def valueToCode(value: float) -> float:
        return -100.0 / value

    @staticmethod
    def readString(s: str) -> OsuSvObj or None:
        if s.isspace():
            return None

        sComma = s.split(",")
        if len(sComma) < 8:
            return None

        this = OsuSvObj()
        this.offset = float(sComma[0])
        this.multiplier = OsuSvObj.codeToValue(float(sComma[1]))
        this.sampleSet = int(sComma[3])
        this.sampleSetIndex = int(sComma[4])
        this.volume = int(sComma[5])
        this.kiai = int(sComma[7])

        return this

    def writeString(self) -> str:
        return f"{int(self.offset)},{self.valueToCode(self.multiplier)}," \
               f"4,{self.sampleSet}," \
               f"{self.sampleSetIndex},{self.volume},{0},{int(self.kiai)}"

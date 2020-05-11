from __future__ import annotations
from reamber.base.HitObject import HitObject
from reamber.osu.OsuHitObjectMeta import OsuHitObjectMeta
from dataclasses import dataclass


@dataclass
class OsuHitObject(HitObject, OsuHitObjectMeta):
    @staticmethod
    def readString(s: str, keys: int) -> OsuHitObject:
        if s.isspace(): return None

        sComma = s.split(",")
        if len(sComma) < 5: return None

        sColon = sComma[-1].split(":")
        if len(sColon) < 5: return None

        this = OsuHitObject()
        this.column = this.xAxisToColumn(int(sComma[0]), keys)
        this.offset = int(sComma[2])
        this.hitsoundSet = int(sComma[4])
        this.sampleSet = int(sColon[0])
        this.additionSet = int(sColon[1])
        this.customSet = int(sColon[2])
        this.volume = int(sColon[3])
        this.hitsoundFile = sColon[4]

        return this

    def writeString(self, keys: int) -> str:
        return f"{OsuHitObjectMeta.columnToXAxis(self.column, keys=keys)},{192}," \
               f"{int(self.offset)},{1},{self.hitsoundSet},{self.sampleSet}:" \
               f"{self.additionSet}:{self.customSet}:{self.volume}:{self.hitsoundFile}"

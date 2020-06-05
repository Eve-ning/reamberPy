from __future__ import annotations
from reamber.base.HoldObject import HoldObject
from reamber.osu.OsuNoteObjectMeta import OsuNoteObjectMeta
from dataclasses import dataclass


@dataclass
class OsuHoldObject(HoldObject, OsuNoteObjectMeta):
    @staticmethod
    def readString(s: str, keys: int) -> OsuHoldObject or None:
        if s.isspace():
            return None

        sComma = s.split(",")
        if len(sComma) < 5:
            return None

        sColon = sComma[-1].split(":")
        if len(sColon) < 6:
            return None

        this = OsuHoldObject()
        this.column = this.xAxisToColumn(int(sComma[0]), keys)
        this.offset = float(sComma[2])
        this.hitsoundSet = int(sComma[4])
        this.length = float(sColon[0]) - this.offset
        this.sampleSet = int(sColon[1])
        this.additionSet = int(sColon[2])
        this.customSet = int(sColon[3])
        this.volume = int(sColon[4])
        this.hitsoundFile = sColon[5]

        return this

    def writeString(self, keys: int) -> str:
        return f"{OsuNoteObjectMeta.columnToXAxis(self.column, keys=keys)},{192}," \
               f"{int(self.offset)},{128},{self.hitsoundSet},{int(self.offset + self.length)}:" \
               f"{self.sampleSet}:{self.additionSet}:{self.customSet}:{self.volume}:{self.hitsoundFile}"

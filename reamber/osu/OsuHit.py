from __future__ import annotations
from reamber.base.HitObj import HitObj
from reamber.osu.OsuNoteObjMeta import OsuNoteObjMeta
from dataclasses import dataclass


@dataclass
class OsuHitObj(HitObj, OsuNoteObjMeta):
    @staticmethod
    def readString(s: str, keys: int) -> OsuHitObj or None:
        """ Reads a single line under the [HitObject] Label. This must explicitly be a Hit Object.

        keys must be specified for conversion of code value to actual column."""
        if s.isspace(): return None

        sComma = s.split(",")
        if len(sComma) < 5: return None

        sColon = sComma[-1].split(":")
        if len(sColon) < 5: return None

        this = OsuHitObj()
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
        """ Exports a .osu writable string """
        return f"{OsuNoteObjMeta.columnToXAxis(self.column, keys=keys)},{192}," \
               f"{int(self.offset)},{1},{self.hitsoundSet},{self.sampleSet}:" \
               f"{self.additionSet}:{self.customSet}:{self.volume}:{self.hitsoundFile}"

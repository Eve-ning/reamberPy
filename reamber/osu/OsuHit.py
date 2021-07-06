from __future__ import annotations

from dataclasses import dataclass

from reamber.base.Hit import Hit
from reamber.osu.OsuNoteMeta import OsuNoteMeta


@dataclass
class OsuHit(Hit, OsuNoteMeta):
    @staticmethod
    def read_string(s: str, keys: int) -> OsuHit or None:
        """ Reads a single line under the [HitObject] Label. This must explicitly be a Hit Object.

        keys must be specified for conversion of code value to actual column."""
        if s.isspace(): return None

        sComma = s.split(",")
        if len(sComma) < 5: return None

        sColon = sComma[-1].split(":")
        if len(sColon) < 5: return None

        this = OsuHit()
        this.column        = this.x_axis_to_column(int(sComma[0]), keys)
        this.offset        = int(sComma[2])
        this.hitsound_set  = int(sComma[4])
        this.sample_set    = int(sColon[0])
        this.addition_set  = int(sColon[1])
        this.custom_set    = int(sColon[2])
        this.volume        = int(sColon[3])
        this.hitsound_file = sColon[4]

        return this

    def write_string(self, keys: int) -> str:
        """ Exports a .osu writable string """
        return f"{OsuNoteMeta.column_to_x_axis(self.column, keys=keys)},{192}," \
               f"{int(self.offset)},{1},{self.hitsound_set},{self.sample_set}:" \
               f"{self.addition_set}:{self.custom_set}:{self.volume}:{self.hitsound_file}"

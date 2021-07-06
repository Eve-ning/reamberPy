from __future__ import annotations

from dataclasses import dataclass, field

from reamber.base.Hold import Hold, HoldTail
from reamber.osu.OsuNoteMeta import OsuNoteMeta


@dataclass
class OsuHoldTail(HoldTail, OsuNoteMeta):
    pass


@dataclass
class OsuHold(Hold, OsuNoteMeta):
    _tail: OsuHoldTail = field(init=False)

    def _upcast_tail(self, **kwargs) -> OsuHoldTail:
        return OsuHoldTail(**kwargs)

    @staticmethod
    def read_string(s: str, keys: int) -> OsuHold or None:
        """ Reads a single line under the [HitObjects] Label. This must explicitly be a Hold Object.

        keys must be specified for conversion of code value to actual column."""
        if s.isspace():
            return None

        s_comma = s.split(",")
        if len(s_comma) < 5:
            return None

        s_colon = s_comma[-1].split(":")
        if len(s_colon) < 6:
            return None

        this = OsuHold()
        this.tail_column(this.x_axis_to_column(int(s_comma[0]), keys))
        this.column        = this.x_axis_to_column(int(s_comma[0]), keys)
        this.offset        = float(s_comma[2])
        this.hitsound_set  = int(s_comma[4])
        this.length        = float(s_colon[0]) - this.offset
        this.sample_set    = int(s_colon[1])
        this.addition_set  = int(s_colon[2])
        this.custom_set    = int(s_colon[3])
        this.volume        = int(s_colon[4])
        this.hitsound_file = s_colon[5]

        return this

    def write_string(self, keys: int) -> str:
        """ Exports a .osu writable string """
        return f"{OsuNoteMeta.column_to_x_axis(self.column, keys=keys)},{192}," \
               f"{int(self.offset)},{128},{self.hitsound_set},{int(self.offset + self.length)}:" \
               f"{self.sample_set}:{self.addition_set}:{self.custom_set}:{self.volume}:{self.hitsound_file}"

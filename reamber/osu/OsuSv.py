from __future__ import annotations

from dataclasses import dataclass

from reamber.base.Timed import Timed
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta

MIN_SV = 0.01
MAX_SV = 10.0

@dataclass
class OsuSv(OsuTimingPointMeta, Timed):
    multiplier: float = 1.0

    @staticmethod
    def code_to_value(code: float) -> float:
        """ Converts the data in the .osu file to the actual SV Value """
        return -100.0 / code

    @staticmethod
    def value_to_code(value: float) -> float:
        """ Converts the actual SV Value to a writable float in .osu """
        return -100.0 / value

    @staticmethod
    def read_string(s: str, safe: bool = True) -> OsuSv or None:
        """ Reads a single line under the [TimingPoints] Label. This must explicitly be a SV Point.

        :param s: String to read
        :param safe: Whether to clip on bad input, e.g. Division By Zero
        """
        if s.isspace(): return None

        s_comma = s.split(",")
        if len(s_comma) < 8: return None

        this = OsuSv()
        assert s_comma[6] == '0', "Unexpected BPM Object in OsuSv."
        this.offset = float(s_comma[0])
        try:
            this.multiplier = OsuSv.code_to_value(float(s_comma[1]))
        except ZeroDivisionError:
            if safe: this.multiplier = MAX_SV
            else: raise ZeroDivisionError("Attempted to load code == 0, leading to Div By Zero")
        this.sample_set = int(s_comma[3])
        this.sample_set_index = int(s_comma[4])
        this.volume = int(s_comma[5])
        this.kiai = int(s_comma[7])

        return this

    def write_string(self, safe: bool = True) -> str:
        """ Exports a .osu writable string

        :param safe: Whether to clip on bad output, e.g. Division By Zero
        """
        try:
            code = self.value_to_code(self.multiplier)
        except ZeroDivisionError:
            if safe: code = MIN_SV
            else: raise ZeroDivisionError("Attempted to load value == 0, leading to Div By Zero")

        return f"{self.offset},{code}," \
               f"4,{self.sample_set}," \
               f"{self.sample_set_index},{self.volume},{0},{int(self.kiai)}"

from __future__ import annotations

from dataclasses import dataclass

from reamber.base.Bpm import Bpm
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta

MAX_BPM = 1e07
MIN_BPM = 1e-07

@dataclass
class OsuBpm(OsuTimingPointMeta, Bpm):
    @staticmethod
    def code_to_value(code: float) -> float:
        """ Converts the data in the .osu file to the actual Bpm Value """
        return 60000.0 / code

    @staticmethod
    def value_to_code(value: float) -> float:
        """ Converts the actual Bpm Value to a writable float in .osu """
        return 60000.0 / value

    @staticmethod
    def read_string(s: str, safe: bool = True) -> OsuBpm or None:
        """ Reads a single line under the [TimingPoints] Label. This must explicitly be a BPM Point.

        :param s: String to read
        :param safe: Whether to clip on bad input, e.g. Division By Zero
        """
        if s.isspace(): return None

        s_comma = s.split(",")
        if len(s_comma) < 8: return None

        this = OsuBpm()
        assert s_comma[6] == '1', "Unexpected SV Object in OsuBpm."
        this.offset = float(s_comma[0])
        try:
            this.bpm = OsuBpm.code_to_value(float(s_comma[1]))
        except ZeroDivisionError:
            if safe: this.bpm = MAX_BPM
            else: raise ZeroDivisionError("Attempted to load code == 0, leading to Div By Zero")
        this.metronome = int(s_comma[2])
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
            code = self.value_to_code(self.bpm)
        except ZeroDivisionError:
            if safe: code = MIN_BPM
            else: raise ZeroDivisionError("Attempted to load value == 0, leading to Div By Zero")

        return f"{self.offset},{code}," \
               f"{self.metronome},{self.sample_set}," \
               f"{self.sample_set_index},{self.volume},{1},{int(self.kiai)}"

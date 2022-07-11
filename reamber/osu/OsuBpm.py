from __future__ import annotations

from reamber.base import item_props
from reamber.base.Bpm import Bpm
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta


@item_props()
class OsuBpm(OsuTimingPointMeta, Bpm):

    def __init__(self,
                 offset: float,
                 bpm: float,
                 metronome: int = 4,
                 sample_set: int = OsuSampleSet.AUTO,
                 sample_set_index: int = 0,
                 volume: int = 50,
                 kiai: bool = False,
                 **kwargs):
        super().__init__(
            offset=offset, bpm=bpm, metronome=metronome, sample_set=sample_set,
            sample_set_index=sample_set_index, volume=volume, kiai=kiai,
            **kwargs
        )

    @staticmethod
    def code_to_value(code: float) -> float:
        """Converts .osu format to actual Bpm"""
        try:
            return 60000.0 / code
        except ZeroDivisionError:
            raise ZeroDivisionError("BPM cannot be infinite.")

    @staticmethod
    def value_to_code(value: float) -> float:
        """Converts actual Bpm .osu format"""
        try:
            return 60000.0 / value
        except ZeroDivisionError:
            raise ZeroDivisionError("BPM cannot be exactly 0.")

    @staticmethod
    def read_string(s: str, as_dict: bool = False) -> OsuBpm:
        """Reads a single line under the [TimingPoints] Label. """
        if not OsuTimingPointMeta.is_timing_point(s):
            raise ValueError(f"Bad OsuBpm format: {s}")

        s_comma = s.split(",")
        d = dict(offset=float(s_comma[0]),
                 bpm=OsuBpm.code_to_value(float(s_comma[1])),
                 metronome=int(s_comma[2]),
                 sample_set=int(s_comma[3]),
                 sample_set_index=int(s_comma[4]),
                 volume=int(s_comma[5]),
                 kiai=bool(int(s_comma[7])))
        return d if as_dict else OsuBpm(**d)
    def write_string(self) -> str:
        """Writes a .osu writable string"""

        return f"{self.offset}," \
               f"{self.value_to_code(self.bpm)}," \
               f"{int(self.metronome)}," \
               f"{int(self.sample_set)}," \
               f"{int(self.sample_set_index)}," \
               f"{int(self.volume)}," \
               f"{1}," \
               f"{int(self.kiai)}"

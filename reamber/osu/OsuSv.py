from __future__ import annotations

from reamber.base import item_props
from reamber.base.Timed import Timed
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta


@item_props()
class OsuSv(OsuTimingPointMeta, Timed):
    _props = dict(multiplier=['float', 1.0])

    def __init__(self,
                 offset: float,
                 multiplier: float = 1.0,
                 metronome: int = 4,
                 sample_set: int = OsuSampleSet.AUTO,
                 sample_set_index: int = 0,
                 volume: int = 50,
                 kiai: bool = False,
                 **kwargs):
        super().__init__(
            offset=offset, multiplier=multiplier, metronome=metronome,
            sample_set=sample_set, sample_set_index=sample_set_index,
            volume=volume, kiai=kiai, **kwargs
        )

    @staticmethod
    def code_to_value(code: float) -> float:
        """Converts the data in the .osu file to the actual SV Value"""
        try:
            return -100.0 / code
        except ZeroDivisionError:
            raise ZeroDivisionError("SV cannot be infinite.")

    @staticmethod
    def value_to_code(value: float) -> float:
        """Converts the actual SV Value to a writable float in .osu"""
        try:
            return -100.0 / value
        except ZeroDivisionError:
            raise ZeroDivisionError("SV cannot be 0.")

    @staticmethod
    def read_string(s: str, as_dict: bool = False) -> OsuSv | dict[str]:
        """Reads a single line under the [TimingPoints] Label"""
        if not OsuTimingPointMeta.is_slider_velocity(s):
            raise ValueError(f"Bad OsuSv Format. {s}")

        s_comma = s.split(",")
        d = dict(offset=float(s_comma[0]),
                 multiplier=OsuSv.code_to_value(float(s_comma[1])),
                 sample_set=int(s_comma[3]),
                 sample_set_index=int(s_comma[4]),
                 volume=int(s_comma[5]),
                 kiai=bool(int(s_comma[7])))
        return d if as_dict else OsuSv(**d)

    def write_string(self) -> str:
        """Exports a .osu writable string"""
        return f"{self.offset}," \
               f"{self.value_to_code(float(self.multiplier))}," \
               f"{4}," \
               f"{int(self.sample_set)}," \
               f"{int(self.sample_set_index)}," \
               f"{int(self.volume)}," \
               f"{0}," \
               f"{int(self.kiai)}"

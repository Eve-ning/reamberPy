from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Union

from reamber.base import item_props
from reamber.base.Timed import Timed
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta

MIN_SV = 0.01
MAX_SV = 10.0

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
            offset=offset, multiplier=multiplier, metronome=metronome, sample_set=sample_set,
            sample_set_index=sample_set_index, volume=volume, kiai=kiai, **kwargs
        )

    @staticmethod
    def code_to_value(code: float) -> float:
        """ Converts the data in the .osu file to the actual SV Value """
        return -100.0 / code

    @staticmethod
    def value_to_code(value: float) -> float:
        """ Converts the actual SV Value to a writable float in .osu """
        return -100.0 / value

    @staticmethod
    def read_string(s: str, as_dict: bool = False) -> Union[OsuSv, Dict[str]]:
        """ Reads a single line under the [TimingPoints] Label. This must explicitly be a SV Point.

        :param s: String to read
        :param as_dict: To return as a dictionary or OsuSv
        """
        if not OsuTimingPointMeta.is_slider_velocity(s):
            raise ValueError(f"String provided is not of the correct format for OsuBpm. {s}")

        s_comma = s.split(",")
        try:
            d = dict(offset=float(s_comma[0]),
                     multiplier=OsuSv.code_to_value(float(s_comma[1])),
                     sample_set=int(s_comma[3]),
                     sample_set_index=int(s_comma[4]),
                     volume=int(s_comma[5]),
                     kiai=bool(int(s_comma[7])))
            return d if as_dict else OsuSv(**d)
        except ZeroDivisionError:
            raise ZeroDivisionError("SV cannot be infinite.")
        except IndexError as e:
            raise ValueError(f"String provided is not of the correct format for OsuSv. {s}, {e.args}")

    def write_string(self) -> str:
        """ Exports a .osu writable string """
        try:
            return f"{self.offset},{self.value_to_code(float(self.multiplier))}," \
                   f"{4},{self.sample_set}," \
                   f"{self.sample_set_index},{self.volume},{0},{int(self.kiai)}"
        except ZeroDivisionError:
            raise ZeroDivisionError("SV cannot be exactly 0.")

    # @property
    # def multiplier(self):
    #     return self.data['multiplier']
    #
    # @multiplier.setter
    # def multiplier(self, val):
    #     self.data['multiplier'] = val
    #

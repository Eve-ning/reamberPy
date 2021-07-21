from __future__ import annotations

from reamber.base import item_props
from reamber.base.Bpm import Bpm
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta

MAX_BPM = 1e07
MIN_BPM = 1e-07

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
            sample_set_index=sample_set_index, volume=volume, kiai=kiai, **kwargs
        )

    @staticmethod
    def code_to_value(code: float) -> float:
        """ Converts the data in the .osu file to the actual Bpm Value """
        return 60000.0 / code

    @staticmethod
    def value_to_code(value: float) -> float:
        """ Converts the actual Bpm Value to a writable float in .osu """
        return 60000.0 / value

    @staticmethod
    def read_string(s: str, as_dict: bool = False) -> OsuBpm:
        """ Reads a single line under the [TimingPoints] Label. This must explicitly be a BPM Point.

        :param s: String to read
        :param as_dict: To return as a dictionary or OsuSv
        """
        if not OsuTimingPointMeta.is_timing_point(s):
            raise ValueError(f"String provided is not of the correct format for OsuBpm. {s}")

        s_comma = s.split(",")
        try:
            d = dict(offset=float(s_comma[0]),
                     bpm=OsuBpm.code_to_value(float(s_comma[1])),
                     metronome=int(s_comma[2]),
                     sample_set=int(s_comma[3]),
                     sample_set_index=int(s_comma[4]),
                     volume=int(s_comma[5]),
                     kiai=bool(int(s_comma[7])))
            return d if as_dict else OsuBpm(**d)
        except ZeroDivisionError:
            raise ZeroDivisionError("BPM cannot be infinite.")
        except IndexError as e:
            raise ValueError(f"String provided is not of the correct format for OsuBpm. {s}, {e.args}")

    def write_string(self) -> str:
        """ Exports a .osu writable string """

        try:
            return f"{self.offset},{self.value_to_code(self.bpm)}," \
                   f"{self.metronome},{self.sample_set}," \
                   f"{self.sample_set_index},{self.volume},{1},{int(self.kiai)}"
        except ZeroDivisionError:
            raise ZeroDivisionError("BPM cannot be exactly 0.")


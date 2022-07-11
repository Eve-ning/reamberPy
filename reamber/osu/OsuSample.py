from __future__ import annotations

from reamber.base import item_props
from reamber.base.Timed import Timed


@item_props()
class OsuSample(Timed):
    """Osu Samples are autoplay hitsounds. Under [Events]

    Not to be confused w/ OsuSampleSet, a class of static variables
    """

    _props = dict(sample_file=['str', ''],
                  volume=['int', 50])

    def __init__(self,
                 offset: float,
                 sample_file: str = '',
                 volume: int = 70,
                 **kwargs):
        super().__init__(offset=offset, sample_file=sample_file, volume=volume,
                         **kwargs)

    @staticmethod
    def read_string(s: str, as_dict: bool = False) -> OsuSample:
        """Reads the string as a sample"""
        s_comma = s.split(",")
        try:
            d = dict(offset=float(s_comma[1]),
                     sample_file=s_comma[3],
                     volume=int(s_comma[4]))
            return d if as_dict else OsuSample(**d)
        except IndexError as e:
            raise ValueError(f"Bad OsuSample format. {s}, {e.args}")

    def write_string(self) -> str:
        """Exports the sample as a string"""
        return f"Sample,{int(self.offset)},0,{self.sample_file},{self.volume}"

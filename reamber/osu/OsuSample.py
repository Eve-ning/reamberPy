from __future__ import annotations

from dataclasses import dataclass

from reamber.base import item_props
from reamber.base.Timed import Timed


@item_props()
class OsuSample(Timed):
    """ Osu Samples are automatically played hitsounds. Under [Events]

    Not to be confused with OsuSampleSet, where that's a class of static variables
    """

    _props = dict(sample_file='str', volume='int')

    def __init__(self,
                 offset: float,
                 sample_file:str = '',
                 volume: int = 70,
                 **kwargs):
        super(OsuSample, self).__init__(offset=offset, sample_file=sample_file, volume=volume, **kwargs)

    @staticmethod
    def read_string(s: str) -> OsuSample:
        """ Reads the string as a sample """
        s_comma = s.split(",")
        try:
            return OsuSample(
                offset=float(s_comma[1]),
                sample_file=s_comma[3],
                volume=int(s_comma[4]),
            )
        except IndexError as e:
            raise ValueError(f"String provided is not of the correct format for OsuSample. {s}, {e.args}")

    def write_string(self) -> str:
        """ Exports the sample as a string

        e.g. Sample,1600,0,"01.wav",70
        """
        return f"Sample,{int(self.offset)},0,{self.sample_file},{self.volume}"

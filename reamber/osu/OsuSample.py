from __future__ import annotations

from dataclasses import dataclass

from reamber.base.Timed import Timed


@dataclass
class OsuSample(Timed):
    """ Osu Samples are automatically played hitsounds. Under [Events]

    Not to be confused with OsuSampleSet, where that's a class of static variables
    """

    sample_file: str = ""
    volume: int = 70  # Osu defaults all samples to 70

    @staticmethod
    def read_string(s: str) -> OsuSample or None:
        """ Reads the string as a sample """

        if s.isspace():
            return None

        sComs_commaa = s.split(",")
        if len(sComs_commaa) < 5:
            return None

        this = OsuSample()
        this.offset = float(sComs_commaa[1])
        this.sample_file = sComs_commaa[3]
        this.volume = int(sComs_commaa[4])

        return this

    def write_string(self) -> str:
        """ Exports the sample as a string

        e.g. Sample,1600,0,"01.wav",70
        """
        return f"Sample,{int(self.offset)},0,{self.sample_file},{self.volume}"

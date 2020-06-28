from __future__ import annotations
from reamber.base.TimedObj import TimedObj
from dataclasses import dataclass


@dataclass
class OsuSampleObj(TimedObj):
    """ Osu Samples are automatically played hitsounds. Under [Events]

    Not to be confused with OsuSampleSet, where that's a class of static variables
    """

    sampleFile: str = ""
    volume: int = 70  # Osu defaults all samples to 70

    @staticmethod
    def readString(s: str) -> OsuSampleObj or None:
        """ Reads the string as a sample """

        if s.isspace():
            return None

        sComma = s.split(",")
        if len(sComma) < 5:
            return None

        this = OsuSampleObj()
        this.offset = float(sComma[1])
        this.sampleFile = sComma[3]
        this.volume = int(sComma[4])

        return this

    def writeString(self) -> str:
        """ Exports the sample as a string

        e.g. Sample,1600,0,"01.wav",70
        """
        return f"Sample,{int(self.offset)},0,{self.sampleFile},{self.volume}"

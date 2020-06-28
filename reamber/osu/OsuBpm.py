from __future__ import annotations
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta
from reamber.base.Bpm import Bpm
from dataclasses import dataclass

MAX_BPM = 1e07
MIN_BPM = 1e-07

@dataclass
class OsuBpm(OsuTimingPointMeta, Bpm):
    @staticmethod
    def codeToValue(code: float) -> float:
        """ Converts the data in the .osu file to the actual Bpm Value """
        return 60000.0 / code

    @staticmethod
    def valueToCode(value: float) -> float:
        """ Converts the actual Bpm Value to a writable float in .osu """
        return 60000.0 / value

    @staticmethod
    def readString(s: str) -> OsuBpm or None:
        """ Reads a single line under the [TimingPoints] Label. This must explicitly be a BPM Point. """
        if s.isspace(): return None

        sComma = s.split(",")
        if len(sComma) < 8: return None

        this = OsuBpm()
        assert sComma[6] == '1', "Unexpected SV Object in OsuBpm."
        this.offset = float(sComma[0])
        this.bpm = OsuBpm.codeToValue(float(sComma[1]))
        this.metronome = int(sComma[2])
        this.sampleSet = int(sComma[3])
        this.sampleSetIndex = int(sComma[4])
        this.volume = int(sComma[5])
        this.kiai = int(sComma[7])

        return this

    def writeString(self) -> str:
        """ Exports a .osu writable string """
        return f"{self.offset},{self.valueToCode(self.bpm)}," \
               f"{self.metronome},{self.sampleSet}," \
               f"{self.sampleSetIndex},{self.volume},{1},{int(self.kiai)}"

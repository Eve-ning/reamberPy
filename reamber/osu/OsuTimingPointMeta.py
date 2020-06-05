from reamber.osu.OsuSampleSet import OsuSampleSet
from dataclasses import dataclass


class OsuTimingPointType:
    SV: int = 0
    Bpm: int = 1


@dataclass
class OsuTimingPointMeta:
    sampleSet: int = OsuSampleSet.AUTO
    sampleSetIndex: int = 0
    volume: int = 50
    kiai: bool = False

    @staticmethod
    def isTimingPoint(s: str) -> bool or None:
        t = s.split(",")
        if len(t) < 8:
            return None
        return t[6] == "1"

    @staticmethod
    def isSliderVelocity(s: str) -> bool or None:
        t = s.split(",")
        if len(t) < 8:
            return None
        return t[6] == "0"


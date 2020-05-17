from reamber.osu.OsuSampleSet import OsuSampleSet
from dataclasses import dataclass
from math import ceil


class OsuHitObjectType:
    NOTE: int = 1
    LONG_NOTE: int = 128


@dataclass
class OsuHitObjectMeta:
    hitsoundSet: int = OsuSampleSet.AUTO
    sampleSet: int = OsuSampleSet.AUTO
    additionSet: int = OsuSampleSet.AUTO
    customSet: int = OsuSampleSet.AUTO
    volume: int = 0
    hitsoundFile: str = ""
    # keys to be supplied by map

    @staticmethod
    def xAxisToColumn(xAxis: float, keys: int) -> int:
        return int(ceil((xAxis * keys - 256.0) / 512.0))

    @staticmethod
    def columnToXAxis(column: float, keys: int) -> int:
        return int(round(((512.0 * column) + 256.0) / keys))

    @staticmethod
    def isHitObject(s: str):
        return s.count(":") == 4

    @staticmethod
    def isHoldObject(s: str):
        return s.count(":") == 5

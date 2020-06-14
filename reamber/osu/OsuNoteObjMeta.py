from reamber.osu.OsuSampleSet import OsuSampleSet
from dataclasses import dataclass
from math import ceil


class OsuNoteObjType:
    NOTE: int = 1
    LONG_NOTE: int = 128


@dataclass
class OsuNoteObjMeta:
    hitsoundSet: int = OsuSampleSet.AUTO
    sampleSet: int = OsuSampleSet.AUTO
    additionSet: int = OsuSampleSet.AUTO
    customSet: int = OsuSampleSet.AUTO
    volume: int = 0
    hitsoundFile: str = ""
    # keys to be supplied by map

    @staticmethod
    def xAxisToColumn(xAxis: float, keys: int, clip: bool = True) -> int:
        """ if clip is true, the return will be clipped to max of (keys - 1) """
        col = int(ceil((xAxis * keys - 256.0) / 512.0))
        return min(keys - 1, col)

    @staticmethod
    def columnToXAxis(column: float, keys: int) -> int:
        return int(round(((512.0 * column) + 256.0) / keys))

    @staticmethod
    def isHitObj(s: str):
        return s.count(":") == 4

    @staticmethod
    def isHoldObj(s: str):
        return s.count(":") == 5

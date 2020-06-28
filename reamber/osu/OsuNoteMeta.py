from reamber.osu.OsuSampleSet import OsuSampleSet
from dataclasses import dataclass
from math import ceil


class OsuNoteObjType:
    NOTE: int = 1
    LONG_NOTE: int = 128


@dataclass
class OsuNoteObjMeta:
    """ Holds all metadata for every note object"""

    hitsoundSet: int = OsuSampleSet.AUTO
    sampleSet: int = OsuSampleSet.AUTO
    additionSet: int = OsuSampleSet.AUTO
    customSet: int = OsuSampleSet.AUTO
    volume: int = 0
    hitsoundFile: str = ""
    # keys to be supplied by map

    @staticmethod
    def xAxisToColumn(xAxis: float, keys: int, clip: bool = True) -> int:
        """ Converts the xAxis code in .osu to an actual column value

        Note that column starts from 0

        :param xAxis: The code in .osu to convert
        :param keys: Required for conversion
        :param clip: If true the return will be clipped to max of (keys - 1)
        :return: The actual column value, starting from 0
        """
        col = int(ceil((xAxis * keys - 256.0) / 512.0))
        return min(keys - 1, col) if clip else col

    @staticmethod
    def columnToXAxis(column: float, keys: int) -> int:
        """ Converts the actual column value to a .osu writable code value

        Note that column starts from 0

        :param column: The column to convert
        :param keys: Required for conversion
        :return: The actual code
        """
        return int(round(((512.0 * column) + 256.0) / keys))

    @staticmethod
    def isHitObj(s: str):
        """ Checks if the string is a HitObject """
        return s.count(":") == 4

    @staticmethod
    def isHoldObj(s: str):
        """ Checks if the string is a HoldObject """
        return s.count(":") == 5

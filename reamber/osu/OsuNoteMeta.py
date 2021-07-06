from dataclasses import dataclass
from math import ceil

from reamber.osu.OsuSampleSet import OsuSampleSet


class OsuNoteType:
    NOTE: int = 1
    LONG_NOTE: int = 128


@dataclass
class OsuNoteMeta:
    """ Holds all metadata for every note object"""

    hitsound_set: int = OsuSampleSet.AUTO
    sample_set: int = OsuSampleSet.AUTO
    addition_set: int = OsuSampleSet.AUTO
    custom_set: int = OsuSampleSet.AUTO
    volume: int = 0
    hitsound_file: str = ""
    # keys to be supplied by map

    @staticmethod
    def x_axis_to_column(x_axis: float, keys: int, clip: bool = True) -> int:
        """ Converts the xAxis code in .osu to an actual column value

        Note that column starts from 0

        :param x_axis: The code in .osu to convert
        :param keys: Required for conversion
        :param clip: If true the return will be clipped to max of (keys - 1)
        :return: The actual column value, starting from 0
        """
        col = int(ceil((x_axis * keys - 256.0) / 512.0))
        return min(keys - 1, col) if clip else col

    @staticmethod
    def column_to_x_axis(column: float, keys: int) -> int:
        """ Converts the actual column value to a .osu writable code value

        Note that column starts from 0

        :param column: The column to convert
        :param keys: Required for conversion
        :return: The actual code
        """
        return int(round(((512.0 * column) + 256.0) / keys))

    @staticmethod
    def is_hit(s: str):
        """ Checks if the string is a HitObject """
        return s.count(":") == 4

    @staticmethod
    def is_hold(s: str):
        """ Checks if the string is a HoldObject """
        return s.count(":") == 5

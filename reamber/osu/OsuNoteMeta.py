from math import ceil, floor

from typing import TYPE_CHECKING

from reamber.base.Property import item_props
from reamber.osu import OsuSampleSet


@item_props()
class OsuNoteMeta:
    """ Holds all metadata for every note object"""

    _props = dict(hitsound_set='int',
                  sample_set='int',
                  addition_set='int',
                  custom_set='int',
                  volume='int',
                  hitsound_file='object')

    def reset_samples(self):
        self.hitsound_set = OsuSampleSet.AUTO
        self.sample_set = OsuSampleSet.AUTO
        self.addition_set = OsuSampleSet.AUTO
        self.custom_set = 0
        self.hitsound_file: str = ""

    @staticmethod
    def x_axis_to_column(x_axis: float, keys: int, clip: bool = True) -> int:
        """ Converts the x_axis code in .osu to an actual column value

        Note that column starts from 0

        :param x_axis: The code in .osu to convert
        :param keys: Required for conversion
        :param clip: If true the return will be clipped to max of (keys - 1)
        :return: The actual column value, starting from 0
        """
        assert keys > 0, f"Keys cannot be negative. {keys}"
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
        assert keys > 0, f"Keys cannot be negative. {keys}"
        return int(floor(((512.0 * column) + 256.0) / keys))

    @staticmethod
    def is_hit(s: str):
        """ Checks if the string is a HitObject """
        return s.count(":") == 4

    @staticmethod
    def is_hold(s: str):
        """ Checks if the string is a HoldObject """
        return s.count(":") == 5

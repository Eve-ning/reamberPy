from math import ceil, floor

from reamber.base.Property import item_props
from reamber.osu.OsuSampleSet import OsuSampleSet


@item_props()
class OsuNoteMeta:
    """Holds all metadata for every note object"""

    _props = dict(hitsound_set=['int', 0],
                  sample_set=['int', 0],
                  addition_set=['int', 0],
                  custom_set=['int', 0],
                  volume=['int', 0],
                  hitsound_file=['object', ""])

    # noinspection PyAttributeOutsideInit
    def reset_samples(self):
        self.hitsound_set = OsuSampleSet.AUTO
        self.sample_set = OsuSampleSet.AUTO
        self.addition_set = OsuSampleSet.AUTO
        self.custom_set = 0
        self.hitsound_file: str = ""

    @staticmethod
    def x_axis_to_column(x_axis: float, keys: int) -> int:
        """Converts the x_axis code in .osu to an actual column value

        Args:
            x_axis: The code in .osu to convert
            keys: Required for conversion

        Returns:
            The actual column value, starting from 0
        """
        return max(min(int(x_axis // (512 / keys)), keys - 1), 0)

    @staticmethod
    def column_to_x_axis(column: float, keys: int) -> int:
        """Converts the actual column value to a .osu writable code value

        Args:
            column: The column to convert starting from 0
            keys: Required for conversion

        Returns:
            The actual code
        """
        assert keys > 0, f"Keys cannot be negative. {keys}"
        return int(floor(((512.0 * column) + 256.0) / keys))

    @staticmethod
    def is_hit(s: str):
        """Checks if the string is a HitObject"""
        return s.count(":") == 4 and s.count(",") == 5

    @staticmethod
    def is_hold(s: str):
        """Checks if the string is a HoldObject"""
        return s.count(":") == 5 and s.count(",") == 5

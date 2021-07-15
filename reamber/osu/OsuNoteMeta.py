from math import ceil, floor

from typing import TYPE_CHECKING

from reamber.osu.OsuSampleSet import OsuSampleSet
if TYPE_CHECKING:
    from reamber.osu import OsuHit


class OsuNoteMeta:
    """ Holds all metadata for every note object"""

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

    @property
    def hitsound_set(self: 'OsuHit'):
        return self.data['hitsound_set']

    @hitsound_set.setter
    def hitsound_set(self: 'OsuHit', value: OsuSampleSet):
        self.data['hitsound_set'] = value

    @property
    def sample_set(self: 'OsuHit'):
        return self.data['sample_set']

    @sample_set.setter
    def sample_set(self: 'OsuHit', value: OsuSampleSet):
        self.data['sample_set'] = value

    @property
    def addition_set(self: 'OsuHit'):
        return self.data['addition_set']

    @addition_set.setter
    def addition_set(self: 'OsuHit', value: OsuSampleSet):
        self.data['addition_set'] = value

    @property
    def custom_set(self: 'OsuHit'):
        return self.data['custom_set']

    @custom_set.setter
    def custom_set(self: 'OsuHit', value: OsuSampleSet):
        self.data['custom_set'] = value

    @property
    def volume(self: 'OsuHit'):
        return self.data['volume']

    @volume.setter
    def volume(self: 'OsuHit', value: int):
        self.data['volume'] = value

    @property
    def hitsound_file(self: 'OsuHit'):
        return self.data['hitsound_file']

    @hitsound_file.setter
    def hitsound_file(self: 'OsuHit', value: int):
        self.data['hitsound_file'] = value

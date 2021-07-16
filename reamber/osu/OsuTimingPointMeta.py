from typing import TYPE_CHECKING

from reamber.osu.OsuSampleSet import OsuSampleSet

if TYPE_CHECKING:
    from reamber.osu.OsuBpm import OsuBpm

class OsuTimingPointType:
    SV: int = 0
    Bpm: int = 1


class OsuTimingPointMeta:
    """ Holds all metadata for every timing point object"""

    @staticmethod
    def is_timing_point(s: str) -> bool:
        """ Checks whether if the string is a Timing Point/Bpm Obj"""
        t = s.split(",")
        if len(t) < 8:
            return False
        return t[6] == "1"

    @staticmethod
    def is_slider_velocity(s: str) -> bool:
        """ Checks whether if the string is a SV Point/SV Obj """
        t = s.split(",")
        if len(t) < 8:
            return False
        return t[6] == "0"

    @property
    def sample_set(self: 'OsuBpm'):
        return self.data['sample_set']

    @sample_set.setter
    def sample_set(self: 'OsuBpm', value: OsuSampleSet):
        self.data['sample_set'] = value

    @property
    def sample_set_index(self: 'OsuBpm'):
        return self.data['sample_set_index']

    @sample_set_index.setter
    def sample_set_index(self: 'OsuBpm', value: OsuSampleSet):
        self.data['sample_set_index'] = value

    @property
    def volume(self: 'OsuBpm'):
        return self.data['volume']

    @volume.setter
    def volume(self: 'OsuBpm', value: int):
        self.data['volume'] = value

    @property
    def kiai(self: 'OsuBpm'):
        return self.data['kiai']

    @kiai.setter
    def kiai(self: 'OsuBpm', value: OsuSampleSet):
        self.data['kiai'] = value
from dataclasses import dataclass

from reamber.osu.OsuSampleSet import OsuSampleSet


class OsuTimingPointType:
    SV: int = 0
    Bpm: int = 1


@dataclass
class OsuTimingPointMeta:
    """ Holds all metadata for every timing point object"""

    sample_set: int = OsuSampleSet.AUTO
    sample_set_index: int = 0
    volume: int = 50
    kiai: bool = False

    @staticmethod
    def is_timing_point(s: str) -> bool or None:
        """ Checks whether if the string is a Timing Point/Bpm Obj"""
        t = s.split(",")
        if len(t) < 8:
            return None
        return t[6] == "1"

    @staticmethod
    def is_slider_velocity(s: str) -> bool or None:
        """ Checks whether if the string is a SV Point/SV Obj """
        t = s.split(",")
        if len(t) < 8:
            return None
        return t[6] == "0"


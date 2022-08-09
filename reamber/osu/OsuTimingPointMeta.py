from reamber.base.Property import item_props

class OsuTimingPointType:
    SV: int = 0
    Bpm: int = 1

@item_props()
class OsuTimingPointMeta:
    """Holds all metadata for every timing point object"""

    _props = dict(sample_set=['int', 0],
                  sample_set_index=['int', 0],
                  volume=['int', 0],
                  kiai=['bool', False])

    @staticmethod
    def is_timing_point(s: str) -> bool:
        """If string is a Timing Point/Bpm Obj"""
        t = s.split(",")
        if len(t) != 8: return False
        return t[6] == "1"

    @staticmethod
    def is_slider_velocity(s: str) -> bool:
        """If string is a SV Obj"""
        t = s.split(",")
        if len(t) != 8: return False
        return t[6] == "0"

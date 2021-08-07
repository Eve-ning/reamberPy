from reamber.base.Bpm import Bpm


class SMBpm(Bpm):
    DEFAULT_BEATS_PER_MEASURE = 4
    def __init__(self, offset: float, bpm: float, **kwargs): ...
    @staticmethod
    def beat_to_mbs(beats: float) -> tuple: ...
    @staticmethod
    def mbs_to_beat(measure: int, beat: int, slot: float) float: ...

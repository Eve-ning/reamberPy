from reamber.base.Bpm import Bpm


class SMBpm(Bpm):
    DEFAULT_BEATS_PER_MEASURE = 4

    @staticmethod
    def beat_to_mbs(beats: float):
        """ Converts beats to measure, beats and slot """
        return int(beats) // 4, int(beats) % 4, beats % 1

    @staticmethod
    def mbs_to_beat(measure: int, beat: int, slot: float):
        return measure * 4 + beat + slot

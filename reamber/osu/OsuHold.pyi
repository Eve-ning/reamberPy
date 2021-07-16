from __future__ import annotations

from reamber.base.Hold import Hold
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.osu.OsuNoteMeta import OsuNoteMeta


class OsuHold(Hold, OsuNoteMeta):
    def __init__(self, offset: float, column: int, length: float, hitsound_set: int = OsuSampleSet.AUTO,
                 sample_set: int = OsuSampleSet.AUTO, addition_set: int = OsuSampleSet.AUTO,
                 custom_set: int = OsuSampleSet.AUTO, volume: int = 0, hitsound_file: str = "", **kwargs): ...
    @staticmethod
    def read_string(s: str, keys: int) -> OsuHold: ...
    def write_string(self, keys: int) -> str: ...


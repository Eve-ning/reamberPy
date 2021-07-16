from __future__ import annotations

from reamber.base.Hit import Hit
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.osu.OsuNoteMeta import OsuNoteMeta


class OsuHit(Hit, OsuNoteMeta):
    def __init__(self, offset: float, column: int, hitsound_set: int = OsuSampleSet.AUTO,
                 sample_set: int = OsuSampleSet.AUTO, addition_set: int = OsuSampleSet.AUTO, custom_set: int = 0,
                 volume: int = 0, hitsound_file: str = "",  **kwargs): ...
    @staticmethod
    def read_string(s: str, keys: int) -> OsuHit: ...
    def write_string(self, keys: int) -> str: ...

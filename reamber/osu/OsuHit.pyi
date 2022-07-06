from __future__ import annotations

from typing import overload, Dict

from reamber.base.Hit import Hit
from reamber.osu.OsuNoteMeta import OsuNoteMeta
from reamber.osu.OsuSampleSet import OsuSampleSet


class OsuHit(Hit, OsuNoteMeta):
    def __init__(self, offset: float, column: int,
                 hitsound_set: int = OsuSampleSet.AUTO,
                 sample_set: int = OsuSampleSet.AUTO,
                 addition_set: int = OsuSampleSet.AUTO, custom_set: int = 0,
                 volume: int = 0, hitsound_file: str = "", **kwargs): ...

    @staticmethod
    @overload
    def read_string(s: str, keys: int, as_dict: bool = False) -> OsuHit: ...

    @staticmethod
    @overload
    def read_string(s: str, keys: int, as_dict: bool = True) -> Dict[str]: ...

    @staticmethod
    def read_string(s: str, keys: int, as_dict: bool = True) -> OsuHit or Dict[
        str]: ...

    def write_string(self, keys: int) -> str: ...

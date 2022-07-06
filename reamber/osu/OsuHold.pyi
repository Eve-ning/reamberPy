from __future__ import annotations

from typing import Dict, overload

from reamber.base.Hold import Hold
from reamber.osu.OsuNoteMeta import OsuNoteMeta
from reamber.osu.OsuSampleSet import OsuSampleSet


class OsuHold(Hold, OsuNoteMeta):
    def __init__(self, offset: float, column: int, length: float,
                 hitsound_set: int = OsuSampleSet.AUTO,
                 sample_set: int = OsuSampleSet.AUTO,
                 addition_set: int = OsuSampleSet.AUTO,
                 custom_set: int = OsuSampleSet.AUTO, volume: int = 0,
                 hitsound_file: str = "", **kwargs): ...

    @staticmethod
    @overload
    def read_string(s: str, keys: int, as_dict: bool = False) -> OsuHold: ...

    @staticmethod
    @overload
    def read_string(s: str, keys: int, as_dict: bool = True) -> Dict[str]: ...

    @staticmethod
    def read_string(s: str, keys: int, as_dict: bool = True) -> OsuHold or \
                                                                Dict[str]: ...

    def write_string(self, keys: int) -> str: ...

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Union

from reamber.base.Map import Map
from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuHit import OsuHit
from reamber.osu.OsuHold import OsuHold
from reamber.osu.OsuMapMeta import OsuMapMeta
from reamber.osu.OsuNoteMeta import OsuNoteMeta
from reamber.osu.OsuSv import OsuSv
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.OsuSvList import OsuSvList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList


@dataclass
class OsuMap(Map[OsuHitList, OsuHoldList, OsuNotePkg, OsuBpmList], OsuMapMeta):

    def reset_all_samples(self, notes=True, samples=True) -> None: ...
    @staticmethod
    def read(lines: List[str]) -> OsuMap: ...
    @staticmethod
    def read_file(file_path: str) -> OsuMap: ...
    def write_file(self, file_path=""): ...
    def _read_file_metadata(self, lines: List[str]): ...
    def _read_file_timing_points(self, lines: Union[List[str], str]): ...

    def _read_file_hit_objects(self, lines: Union[List[str], str]): ...
    def scroll_speed(self, center_bpm: float = None) -> List[Dict[str, float]]: ...

    # noinspection PyMethodOverriding
    def metadata(self, unicode=True) -> str: ...
    def rate(self, by: float, inplace:bool = False): ...
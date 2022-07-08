from __future__ import annotations

from dataclasses import dataclass
from typing import List, Union, Tuple, TypeVar, Type

import pandas as pd

from reamber.base.Map import Map
from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuMapMeta import OsuMapMeta
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuSvList import OsuSvList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList

T = TypeVar('T', bound=TimedList)


@dataclass
class OsuMap(Map[OsuNoteList, OsuHitList, OsuHoldList, OsuBpmList],
             OsuMapMeta):

    @property
    def svs(self) -> OsuSvList: ...

    @svs.setter
    def svs(self, val) -> None: ...

    def reset_samples(self, notes=True, samples=True) -> None: ...

    @staticmethod
    def read(lines: List[str]) -> OsuMap: ...

    @staticmethod
    def read_file(file_path: str) -> OsuMap: ...

    def write(self) -> List[str]: ...

    def write_file(self, file_path="") -> None: ...

    def _read_file_metadata(self, lines: List[str]): ...

    def _read_file_timing_points(self, lines: Union[List[str], str]): ...

    def _read_file_hit_objects(self, lines: Union[List[str], str]): ...

    def metadata(self, unicode=True, **kwargs) -> str: ...

    def rate(self, by: float) -> OsuMap: ...

    class Stacker(Map.Stacker):
        @property
        def hitsound_set(self) -> pd.Series: ...

        @hitsound_set.setter
        def hitsound_set(self, val) -> None: ...

        @property
        def sample_set(self) -> pd.Series: ...

        @sample_set.setter
        def sample_set(self, val) -> None: ...

        @property
        def addition_set(self) -> pd.Series: ...

        @addition_set.setter
        def addition_set(self, val) -> None: ...

        @property
        def custom_set(self) -> pd.Series: ...

        @custom_set.setter
        def custom_set(self, val) -> None: ...

        @property
        def volume(self) -> pd.Series: ...

        @volume.setter
        def volume(self, val) -> None: ...

        @property
        def hitsound_file(self) -> pd.Series: ...

        @hitsound_file.setter
        def hitsound_file(self, val) -> None: ...

        @property
        def sample_set_index(self) -> pd.Series: ...

        @sample_set_index.setter
        def sample_set_index(self, val) -> None: ...

        @property
        def kiai(self) -> pd.Series: ...

        @kiai.setter
        def kiai(self, val) -> None: ...

    def stack(self, include_types: Tuple[Type[T]] = None) -> Stacker: ...

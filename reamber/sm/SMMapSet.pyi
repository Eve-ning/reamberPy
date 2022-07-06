from __future__ import annotations

from dataclasses import dataclass
from typing import List, Iterator

from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.base.MapSet import MapSet
from reamber.sm.SMMap import SMMap
from reamber.sm.SMMapSetMeta import SMMapSetMeta
from reamber.sm.lists import SMStopList
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.notes import SMNoteList, SMHitList, SMHoldList


@dataclass
class SMMapSet(MapSet[SMNoteList, SMHitList, SMHoldList, SMBpmList, SMMap],
               SMMapSetMeta):

    def __iter__(self) -> Iterator[SMMap]: ...

    @staticmethod
    def read(lines: str | List[str]) -> SMMapSet: ...

    @staticmethod
    def read_file(file_path: str) -> SMMapSet: ...

    def write(self) -> str: ...

    def write_file(self, file_path: str): ...

    def _read_maps(self, maps: List[str],
                   bcs_s: List[BpmChangeSnap],
                   stops: SMStopList): ...

    # noinspection PyTypeChecker
    def rate(self, by: float) -> SMMapSet: ...

from __future__ import annotations

from ctypes import Union
from dataclasses import dataclass
from typing import List

from reamber.base.MapSet import MapSet
from reamber.sm.SMMap import SMMap
from reamber.sm.SMMapSetMeta import SMMapSetMeta
from reamber.sm.SMStop import SMStop
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.notes import SMNoteList, SMHitList, SMHoldList


@dataclass
class SMMapSet(MapSet[SMNoteList, SMHitList, SMHoldList, SMBpmList, SMMap], SMMapSetMeta):

    @staticmethod
    def read(lines: Union[str, List[str]]) -> SMMapSet: ...
    @staticmethod
    def read_file(file_path: str) -> SMMapSet: ...

    def write_file(self, file_path: str): ...

    def _read_maps(self, maps: List[str], bpms: SMBpmList, stops: List[SMStop]): ...
    # noinspection PyTypeChecker
    def rate(self, by: float) -> SMMapSet: ...

    class Stacker(MapSet.Stacker): ...
    @property
    def stack(self) -> Stacker: ...



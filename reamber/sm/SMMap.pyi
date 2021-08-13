from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, TYPE_CHECKING

from reamber.base.Map import Map
from reamber.base.lists import TimedList
from reamber.sm.SMMapMeta import SMMapMeta
from reamber.sm.SMStop import SMStop
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.SMStopList import SMStopList
from reamber.sm.lists.notes import SMNoteList, SMHitList, SMHoldList, SMFakeList, SMLiftList, SMKeySoundList, \
    SMMineList, SMRollList

if TYPE_CHECKING:
    from reamber.sm.SMMapSet import SMMapSet


import logging
log = logging.getLogger(__name__)


@dataclass
class SMMap(Map[SMNoteList, SMHitList, SMHoldList, SMBpmList], SMMapMeta):
    """ If you're trying to load using this, use SMMapSet. """

    objs: Dict[str, TimedList] = field(init=False, default_factory=...)

    @property
    def fakes(self) -> SMFakeList: ...
    @fakes.setter
    def fakes(self, val) -> None: ...
    @property
    def lifts(self) -> SMLiftList: ...
    @lifts.setter
    def lifts(self, val) -> None: ...
    @property
    def keysounds(self) -> SMKeySoundList: ...
    @keysounds.setter
    def keysounds(self, val) -> None: ...
    @property
    def mines(self) -> SMMineList: ...
    @mines.setter
    def mines(self, val) -> None: ...
    @property
    def rolls(self) -> SMRollList: ...
    @rolls.setter
    def rolls(self, val) -> None: ...
    @property
    def stops(self) -> SMStopList: ...
    @stops.setter
    def stops(self, val) -> None: ...

    _SNAP_ERROR_BUFFER = 0.001

    @staticmethod
    def read_string(note_str: str, bpms: SMBpmList, stops: List[SMStop]) -> SMMap: ...
    def write_string(self) -> List[str]: ...
    def _read_notes(self, measures: List[List[str]]): ...

    # noinspection PyMethodOverriding
    def metadata(self, s:SMMapSet, unicode=True) -> str: ...

    # noinspection PyMethodOverriding
    def describe(self, s:SMMapSet, rounding: int = 2, unicode: bool = False) -> str: ...
    def rate(self, by: float, inplace:bool = False) -> SMMap: ...

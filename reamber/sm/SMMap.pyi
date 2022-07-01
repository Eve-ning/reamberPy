from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, TYPE_CHECKING

from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.base.Map import Map
from reamber.base.lists import TimedList
from reamber.sm.SMMapMeta import SMMapMeta
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.SMStopList import SMStopList
from reamber.sm.lists.notes import SMNoteList, SMHitList, SMHoldList, \
    SMFakeList, SMLiftList, SMKeySoundList, \
    SMMineList, SMRollList

if TYPE_CHECKING:
    from reamber.sm.SMMapSet import SMMapSet

@dataclass
class SMMap(Map[SMNoteList, SMHitList, SMHoldList, SMBpmList], SMMapMeta):
    objs: Dict[str, TimedList] = field(init=False,
                                       default_factory=...)

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

    @staticmethod
    def read(s: str,
             bcs_s: List[BpmChangeSnap],
             initial_offset: float,
             stops: SMStopList) -> SMMap: ...

    def write(self) -> List[str]: ...

    def _read_notes(self,
                    note_data: str,
                    initial_offset: float,
                    bcs_s: List[BpmChangeSnap],
                    stops: SMStopList): ...

    # noinspection PyMethodOverriding
    def metadata(self, s: SMMapSet, unicode=True) -> str: ...

    # noinspection PyMethodOverriding
    def describe(self, s: SMMapSet, rounding: int = 2,
                 unicode: bool = False) -> str: ...

    def rate(self, by: float, inplace: bool = False) -> SMMap: ...

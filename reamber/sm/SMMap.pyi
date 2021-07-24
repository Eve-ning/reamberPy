from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, TYPE_CHECKING

from reamber.base.Map import Map
from reamber.base.Property import map_props
from reamber.base.lists import TimedList
from reamber.sm.SMBpm import SMBpm
from reamber.sm.SMConst import SMConst
from reamber.sm.SMFake import SMFake
from reamber.sm.SMHit import SMHit
from reamber.sm.SMHold import SMHold
from reamber.sm.SMKeySound import SMKeySound
from reamber.sm.SMLift import SMLift
from reamber.sm.SMMapMeta import SMMapMeta, SMMapChartTypes
from reamber.sm.SMMine import SMMine
from reamber.sm.SMRoll import SMRoll
from reamber.sm.SMStop import SMStop
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.notes import SMNoteList, SMHitList, SMHoldList, SMFakeList, SMLiftList, SMKeySoundList, \
    SMMineList, SMRollList

if TYPE_CHECKING:
    from reamber.sm.SMMapSet import SMMapSet

from numpy import gcd

import logging
log = logging.getLogger(__name__)


@dataclass
class SMMap(Map[SMNoteList, SMHitList, SMHoldList, SMBpmList], SMMapMeta):
    """ If you're trying to load using this, use SMMapSet. """

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

    _SNAP_ERROR_BUFFER = 0.001

    @staticmethod
    def read_string(note_str: str, bpms: SMBpmList, stops: List[SMStop]) -> SMMap: ...
    def write_string(self) -> List[str]: ...
    def _read_notes(self, measures: List[List[str]], bpms: SMBpmList, stops: List[SMStop]): ...
    def metadata(self, s: SMMapSet, unicode=True) -> str: ...
    def describe(self, s:SMMapSet, rounding: int = 2, unicode: bool = False) -> str: ...
    def rate(self, by: float, inplace:bool = False) -> SMMap: ...
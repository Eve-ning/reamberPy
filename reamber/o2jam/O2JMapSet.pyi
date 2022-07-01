from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterator, List

from reamber.base.MapSet import MapSet
from reamber.o2jam.O2JMap import O2JMap
from reamber.o2jam.O2JMapSetMeta import O2JMapSetMeta
from reamber.o2jam.lists.O2JBpmList import O2JBpmList
from reamber.o2jam.lists.notes import O2JHitList
from reamber.o2jam.lists.notes.O2JHoldList import O2JHoldList
from reamber.o2jam.lists.notes.O2JNoteList import O2JNoteList

log = logging.getLogger(__name__)


@dataclass
class O2JMapSet(MapSet[O2JNoteList, O2JHitList,
                       O2JHoldList, O2JBpmList, O2JMap], O2JMapSetMeta):
    def __iter__(self) -> Iterator[O2JMap]: ...

    def level_name(self, o2j: O2JMap) -> int: ...

    @staticmethod
    def read(b: bytes) -> O2JMapSet: ...

    @staticmethod
    def read_file(file_path: str) -> O2JMapSet: ...

    class Stacker(MapSet.Stacker): ...

    def stack(self, include: List[str] = None) -> Stacker: ...

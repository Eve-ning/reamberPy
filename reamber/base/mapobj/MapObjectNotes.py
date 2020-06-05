from __future__ import annotations
from reamber.base.mapobj.notes.MapObjectNoteBase import MapObjectNoteBase
from abc import abstractmethod
from typing import Tuple, List


class MapObjectNotes:

    # Inherited classes must guarantee hits and holds are defined
    hits: MapObjectNoteBase
    holds: MapObjectNoteBase

    @abstractmethod
    def columns(self) -> List[int]: ...

    @abstractmethod
    def offsets(self) -> List[float]: ...

    @abstractmethod
    def data(self) -> List: ...

    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def __iter__(self): ...

    @abstractmethod
    def firstOffset(self) -> float: ...

    @abstractmethod
    def lastOffset(self) -> float: ...

    @abstractmethod
    def firstLastOffset(self) -> Tuple[float, float]: ...

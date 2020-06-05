from __future__ import annotations
from reamber.base.mapobj.notes.MapObjectNoteBase import MapObjectNoteBase
from reamber.base.NoteObject import NoteObject
from abc import abstractmethod
from typing import Tuple, List
import pandas as pd
from dataclasses import asdict


class MapObjectNotes:

    # Inherited classes must guarantee hits and holds are defined
    hits: MapObjectNoteBase
    holds: MapObjectNoteBase

    @abstractmethod
    def data(self) -> List[NoteObject]: ...

    def df(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(obj) for obj in self.data()])

    def __len__(self) -> int:
        return len(self.data())

    def __iter__(self):
        yield from self.data()

    def columns(self) -> List[int]:
        return [obj.column for obj in self.data()]

    def maxColumns(self) -> int:
        return max(self.columns())

    def offsets(self) -> List[float]:
        return [obj.offset for obj in self.data()]

    def firstOffset(self) -> float:
        return min(self.offsets())

    def lastOffset(self) -> float:
        return max(self.offsets())

    def firstLastOffset(self) -> Tuple[float, float]:
        sort = sorted(self.offsets())
        return min(sort), max(sort)

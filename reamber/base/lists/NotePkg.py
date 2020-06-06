from __future__ import annotations
from reamber.base.lists.notes.NoteList import NoteList
from reamber.base.NoteObj import NoteObj
from abc import abstractmethod
from typing import Tuple, List
import pandas as pd
from dataclasses import asdict
from copy import deepcopy


class NotePkg:
    """ A Package holds multiple lists """
    # Inherited classes must guarantee hits and holds are defined
    hits: NoteList
    holds: NoteList

    @abstractmethod
    def data(self) -> List[NoteObj]: ...

    def deepcopy(self) -> NotePkg:
        return deepcopy(self)

    def df(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(obj) for obj in self.data()])

    def __len__(self) -> int:
        return len(self.data())

    @abstractmethod
    def __iter__(self): ...

    def addOffset(self, by) -> None:
        for var in vars(self).values():
            print(var)

    def inColumns(self, columns: List[int], inplace: bool = False) -> NotePkg or None:
        if inplace:
            for var in self:
                var.inColumns(columns, inplace=True)
        else:
            s = self.deepcopy()
            for var in s:
                var.inColumns(columns, inplace=False)
            return s

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

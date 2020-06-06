from __future__ import annotations
from reamber.base.lists.notes.NoteList import NoteList
from abc import abstractmethod
from typing import Tuple, List, Dict, Any
import pandas as pd
from dataclasses import asdict
from copy import deepcopy


class NotePkg:
    """ A Package holds multiple lists """

    @abstractmethod
    def data(self) -> Dict[str, NoteList]: ...

    @abstractmethod
    def _upcast(self, dataDict: Dict[str, NoteList]) -> NotePkg: ...
    """ This just upcasts the current class so that inplace methods can work """

    def deepcopy(self) -> NotePkg:
        return deepcopy(self)

    def df(self) -> Dict[str, pd.DataFrame]:
        # noinspection PyDataclass
        return {key: pd.DataFrame(asdict(data)) for key, data in self.data().items()}

    def __len__(self) -> int:
        # return sum([len(dataDict) for dataDict in self.data()])
        return len(self.data())

    def __iter__(self):
        yield from self.data()

    def method(self, method: str, **kwargs) -> Dict[str, Any]:
        return {key: eval(f"_.{method}(" + ",".join([f"{k}={v}" for k, v in kwargs]) + ")")
                for key, _ in self.data().items()}

    def addOffset(self, by, inplace: bool = False) -> NotePkg or None:
        if inplace: self.method('addOffset', by=by, inplace=True)
        else: return self._upcast(self.method('addOffset', by=by, inplace=False))

    def inColumns(self, columns: List[int], inplace: bool = False) -> NotePkg or None:
        if inplace: self.method('addOffset', columns=columns, inplace=True)
        else: return self._upcast(self.method('addOffset', columns=columns, inplace=False))

    def columns(self) -> Dict[str, List[int]]:
        return self.method('columns')

    def maxColumns(self) -> int:
        return max(self.method('maxColumns').values())

    def offsets(self) -> Dict[str, List[float]]:
        return self.method('offsets')

    def firstOffset(self) -> float:
        return min(self.method('firstOffset').values())

    def lastOffset(self) -> float:
        return max(self.method('lastOffset').values())

    def firstLastOffset(self) -> Tuple[float, float]:
        offsets = [i for j in self.offsets().values() for i in j]  # Flattens the offset list
        return min(offsets), max(offsets)

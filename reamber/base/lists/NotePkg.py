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
        # noinspection PyDataclass,PyTypeChecker
        return {key: pd.DataFrame([asdict(obj) for obj in data]) for key, data in self.data().items()}

    def __len__(self) -> int:
        # return sum([len(dataDict) for dataDict in self.data()])
        return len(self.data())

    def objCount(self) -> int:
        return sum([len(data) for data in self.data()])

    def __iter__(self):
        yield from self.data()

    def method(self, method: str, **kwargs) -> Dict[str, Any]:
        expression = f"_.{method}(" + ",".join([f"{k}={v}" for k, v in kwargs.items()]) + ")"
        asFunc = eval('lambda _: ' + expression)
        return {key: asFunc(_) for key, _ in self.data().items()}

        # The above is faster for some reason
        # return {key: eval(f"_.{method}(" + ",".join([f"{k}={v}" for k, v in kwargs.items()]) + ")")
        #         for key, _ in self.data().items()}

    def addOffset(self, by, inplace: bool = False) -> NotePkg:
        if inplace: self.method('addOffset', by=by, inplace=False)
        else: return self._upcast(self.method('addOffset', by=by, inplace=False))

    def inColumns(self, columns: List[int], inplace: bool = False) -> NotePkg:
        if inplace: self.method('inColumns', columns=columns, inplace=False)
        else: return self._upcast(self.method('inColumns', columns=columns, inplace=False))

    def columns(self) -> Dict[str, List[int]]:
        return self.method('columns')

    def maxColumn(self) -> int:
        return max(self.method('maxColumn').values())

    def offsets(self) -> Dict[str, List[float]]:
        return self.method('offsets')

    def firstOffset(self) -> float:
        return min(self.method('firstOffset').values())

    def lastOffset(self) -> float:
        return max(self.method('lastOffset').values())

    def firstLastOffset(self) -> Tuple[float, float]:
        if len(self.offsets()) == 0: return 0.0, float("inf")
        offsets = [i for j in self.offsets().values() for i in j]  # Flattens the offset list
        return min(offsets), max(offsets)

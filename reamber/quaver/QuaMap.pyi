from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Union, Tuple, TypeVar, Type

import pandas as pd

from reamber.base.Map import Map
from reamber.base.lists.TimedList import TimedList
from reamber.quaver.QuaMapMeta import QuaMapMeta
from reamber.quaver.lists.QuaBpmList import QuaBpmList
from reamber.quaver.lists.QuaSvList import QuaSvList
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList

T = TypeVar('T', bound=TimedList)


@dataclass
class QuaMap(Map[QuaNoteList, QuaHitList, QuaHoldList, QuaBpmList],
             QuaMapMeta):
    _props = dict(svs=QuaSvList)
    objs: Dict[str, TimedList] = field(init=False, default_factory=...)

    @property
    def svs(self) -> QuaSvList: ...

    @svs.setter
    def svs(self, val) -> None: ...

    @staticmethod
    def read(lines: Union[List[str], str], safe: bool = True) -> QuaMap: ...

    @staticmethod
    def read_file(file_path: str) -> QuaMap: ...

    def write(self) -> str: ...

    def write_file(self, file_path: str) -> None: ...

    def _read_bpms(self, bpms: List[Dict]) -> None: ...

    def _read_svs(self, svs: List[Dict]) -> None: ...

    def _read_notes(self, notes: List[Dict]) -> None: ...

    # noinspection PyMethodOverriding
    def metadata(self, unicode=True) -> str: ...

    def rate(self, by: float): ...

    class Stacker(Map.Stacker):
        @property
        def keysounds(self) -> pd.Series: ...

        @keysounds.setter
        def keysounds(self, val) -> None: ...

    def stack(self, include_types: Tuple[Type[T]] = None) -> Stacker: ...

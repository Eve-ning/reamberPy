from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, TypeVar, Generic, Dict, Type, Tuple

import pandas as pd
from pandas.core.indexing import _LocIndexer

from reamber.base.lists.BpmList import BpmList
from reamber.base.lists.TimedList import TimedList
from reamber.base.lists.notes.HitList import HitList
from reamber.base.lists.notes.HoldList import HoldList
from reamber.base.lists.notes.NoteList import NoteList

NoteListT = TypeVar('NoteListT', bound=NoteList)
HitListT = TypeVar('HitListT', bound=HitList)
HoldListT = TypeVar('HoldListT', bound=HoldList)
BpmListT = TypeVar('BpmListT', bound=BpmList)

T = TypeVar('T', bound=TimedList)


@dataclass
class Map(Generic[NoteListT, HitListT, HoldListT, BpmListT]):
    """This class should be inherited by all Map Objects

    They must inherit the data method, which extracts all data they hold.
    They are also assumed to be a TimedList.
    """

    objs: Dict[str, TimedList] = field(default_factory=lambda: [])

    def __getitem__(self, item: Type[T]) -> List[Type[T]]: ...

    def __setitem__(self, key: T, value: List[Type[T]]): ...

    @property
    def hits(self) -> HitListT: ...

    @hits.setter
    def hits(self, val) -> None: ...

    @property
    def holds(self) -> HoldListT: ...

    @holds.setter
    def holds(self, val) -> None: ...

    @property
    def bpms(self) -> BpmListT: ...

    @bpms.setter
    def bpms(self, val) -> None: ...

    @property
    def notes(self) -> List[NoteListT]: ...

    @notes.setter
    def notes(self, val: List[NoteListT]) -> None: ...

    def deepcopy(self) -> Map: ...

    def metadata(self, unicode=True, **kwargs) -> str: ...

    def describe(self, rounding: int = 2, **kwargs) -> str: ...

    def rate(self, by: float) -> Map: ...

    class Stacker:
        _ixs: List[int]
        _unstacked: List[TimedList]

        # The stacked property is a concat of all lists, this makes the common ops possible.
        _stacked: pd.DataFrame

        def __init__(self, objs: List[TimedList]): ...

        def _update(self): ...

        def __getitem__(self, item): ...

        def __setitem__(self, key, value): ...

        @property
        def offset(self) -> pd.Series: ...

        @offset.setter
        def offset(self, val: pd.Series): ...

        @property
        def column(self) -> pd.Series: ...

        @column.setter
        def column(self, val: pd.Series): ...

        @property
        def length(self) -> pd.Series: ...

        @length.setter
        def length(self, val: pd.Series): ...

        @property
        def bpm(self) -> pd.Series: ...

        @bpm.setter
        def bpm(self, val: pd.Series): ...

        @property
        def metronome(self) -> pd.Series: ...

        @metronome.setter
        def metronome(self, val: pd.Series): ...

        @property
        def loc(self) -> Map.Stacker.StackerLocIndexer: ...

        @dataclass
        class StackerLocIndexer:
            loc: _LocIndexer
            stacker: Map.Stacker

            def __setitem__(self, key, value): ...

            def __getitem__(self, item): ...

    def stack(self, include_types: Tuple[Type[T]] = None) -> Stacker: ...

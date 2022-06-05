from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Iterator, TypeVar, Union, Any, Generator, Tuple, \
    overload, Generic, Type, Sequence

import numpy as np
import pandas as pd

from reamber.base.Map import Map
from reamber.base.lists import TimedList
from reamber.base.lists.BpmList import BpmList
from reamber.base.lists.notes.HitList import HitList
from reamber.base.lists.notes.HoldList import HoldList
from reamber.base.lists.notes.NoteList import NoteList

NoteListT = TypeVar('NoteListT', bound=NoteList)
HitListT = TypeVar('HitListT', bound=HitList)
HoldListT = TypeVar('HoldListT', bound=HoldList)
BpmListT = TypeVar('BpmListT', bound=BpmList)
MapT = TypeVar('MapT', bound=Map)

T = TypeVar('T', bound=TimedList)
TSlice = TypeVar('TSlice', bound=Sequence)


@dataclass
class MapSet(Generic[NoteListT, HitListT, HoldListT, BpmListT, MapT]):
    maps: List[MapT[NoteListT, HitListT, HoldListT, BpmListT]] = field(
        default_factory=lambda: [])

    def __init__(self, maps: List[
        Map[NoteListT, HitListT, HoldListT, BpmListT]]): ...

    def __iter__(self) -> Iterator[Map]: ...

    def items(self) -> Generator[Tuple[type, Map]]: ...

    @overload
    def __getitem__(self, item: Type[T]) -> List[Type[T]]: ...

    @overload
    def __getitem__(self, item: slice) -> List[Map]: ...

    @overload
    def __getitem__(self, item: int) -> Map: ...

    def __getitem__(self, item: int | slice | Type[T]) -> Map: Map | Sequence[
        Map] | List[Type[T]]

    def __setitem__(self, key: Union[Any, type], value): ...

    def deepcopy(self) -> MapSet: ...

    def describe(self, rounding: int = 2, unicode: bool = False) -> List[
        str]: ...

    def rate(self, by: float) -> MapSet: ...

    class Stacker:
        _ixs: np.ndarray
        _unstacked: List[List[TimedList]]
        _stacked: pd.DataFrame
        _stacks: List

        def __init__(self, maps: List[Map]): ...

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

    def stack(self) -> Stacker: ...

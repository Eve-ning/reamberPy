from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, Iterator, TypeVar, Union, Any, Generic, Type

import pandas as pd

from reamber.base.Map import Map
from reamber.base.Property import stack_props
from reamber.base.lists import TimedList

NoteListT = TypeVar('NoteListT')
HitListT = TypeVar('HitListT')
HoldListT = TypeVar('HoldListT')
BpmListT = TypeVar('BpmListT')
MapT = TypeVar('MapT')

T = TypeVar('T', bound=TimedList)


@dataclass
class MapSet(Generic[NoteListT, HitListT, HoldListT, BpmListT, MapT]):
    maps: List[MapT[NoteListT, HitListT, HoldListT, BpmListT]] = field(
        default_factory=lambda: []
    )

    def __init__(self,
                 maps: List[MapT[NoteListT, HitListT, HoldListT, BpmListT]]):
        self.maps = maps

    def __iter__(self) -> Iterator[MapT]:
        for m in self.maps:
            yield m

    def items(self):
        for m in self.maps:
            yield m.__class__, m

    def __getitem__(self, item: Type[T] | int) -> List[Type[T]]:
        if isinstance(item, type):
            return [m[item][0] for m in self.maps]
        else:
            return self.maps[item]

    def __setitem__(self, key: Union[Any, type], value):
        this = self[key]
        if len(this) != len(value):
            raise ValueError("Length to set mismatched.")
        for i in range(len(this)): this[i] = value[i]

    def deepcopy(self):
        """Returns a deep copy of itself"""
        return deepcopy(self)

    def describe(self, rounding: int = 2, unicode: bool = False) -> List[str]:
        """Describes the map's attributes as a short summary

        Examples:
            >>> from reamber.base import Hit, Bpm
            >>> from reamber.base.lists import BpmList
            >>> from reamber.base.lists.notes import HitList
            >>> bpms = [Bpm(offset=1000, bpm=120)]
            >>> hits = [Hit(offset=1000, column=1),
            ...         Hit(offset=2000, column=2)]
            >>> m = Map()
            ... m.hits = HitList(hits)
            ... m.bpms = BpmList(bpms)
            >>> MapSet([m, m]).describe() # doctest: +ELLIPSIS
            ["...", "..."]

            .. code-block::

                Average BPM: 120.0
                Map Length: 0:00:01

                --- Notes ---
                HitList
                Index(['offset', 'column'], dtype='object')
                ...

                HoldList
                Index(['length', 'column', 'offset'], dtype='object')
                ...

        Args:
            rounding: The decimal rounding
            unicode: Whether to use unicode if available.
        """

        return [m.describe(rounding=rounding, unicode=unicode, s=self)
                for m in self]

    def rate(self, by: float) -> MapSet:
        """Changes the rate of the map

        Examples:
            The following will uprate the map by 10%

            >>> MapSet([]).rate(1.1) # doctest: +ELLIPSIS
            MapSet(...)

        Args:
            by: The rate.
        """
        copy = self.deepcopy()
        copy.maps = [m.rate(by=by) for m in copy.maps]
        return copy

    # noinspection DuplicatedCode,PyUnresolvedReferences
    @stack_props()
    class Stacker:
        """Stacking merges multiple ``TimedList`` to map operations on them.

        Notes:
            Unlike ``Map.Stacker`` this doesn't support conditional indexing.

        Examples:

            >>> from reamber.base.lists import BpmList
            >>> from reamber.base.lists.notes import HitList
            >>> from reamber.base import Hit
            >>> hits = [Hit(offset=1000, column=1),
            ...         Hit(offset=2000, column=2)]
            >>> m = Map()
            >>> m.hits = HitList(hits)
            >>> ms = MapSet([m, m.deepcopy()])
            >>> stack = ms.stack()

            Multiply all offsets in the map by 2

            ``stack.offset`` is a ``pd.DataFrame``.

            ``iloc[0]`` yields the first map offsets

            >>> stack.offset *= 2
            >>> stack.offset.iloc[0].tolist()
            [2000.0, 4000.0]

            Or if you do it inline,

            ``ms[0]`` yields the first map

            >>> ms.stack().offset *= 2
            >>> ms[0].hits.offset.tolist()
            [4000.0, 8000.0]

            Notice that ``stack`` changes the map directly by reference.

            If the property, like ``column``, doesn't exist for ``Bpm``,
            it will simply skip it for ``Bpm``.

            However, all properties must exist at least once.

        """

        """See Map.stack for details"""

        stackers: List[Map.Stacker]

        # noinspection PyProtectedMember
        def __init__(self, stackers: List[Map.Stacker]):
            self.stackers = stackers

        def __getitem__(self, item):
            return pd.DataFrame([i[item] for i in self.stackers])

        def __setitem__(self, key, value):
            for s, i in zip(self.stackers, value.iloc):
                s[key] = i

        _props = ['offset', 'column', 'length', 'bpm', 'metronome']

    def stack(self):
        """Stacks map and includes specific columns

        Examples:

            This will generate a stacker ``stack``

            >>> from reamber.base import Hit
            >>> from reamber.base.lists.notes import HitList
            >>> hits = [Hit(offset=1000, column=1),
            ...         Hit(offset=2000, column=2),
            ...         Hit(offset=3000, column=3)]
            >>> m = Map()
            >>> m.hits = HitList(hits)
            >>> MapSet([m, m.deepcopy()]).stack() # doctest: +ELLIPSIS
            <MapSet.MapSet.Stacker ...>

        Returns:
            A ``MapSet.Stacker`` instance. This is a pass by reference.
            Thus, modifications on the stack will change the map directly.

        """
        return self.Stacker([_.stack() for _ in self])

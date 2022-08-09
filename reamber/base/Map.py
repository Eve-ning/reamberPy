from __future__ import annotations

import datetime
from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, Dict, Type, Generic, Tuple
from typing import TypeVar

import pandas as pd
from pandas.core.indexing import _LocIndexer

from reamber.base.Property import stack_props, map_props
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
@map_props()
class Map(Generic[NoteListT, HitListT, HoldListT, BpmListT]):
    """This class should be inherited by all Map Objects

    They must inherit the data method, which extracts all data they hold.
    They are also assumed to be a TimedList.
    """

    _props = dict(hits=HitList, holds=HoldList, bpms=BpmList)

    # objs is the objects of the class, it MUST be defined,
    # and must have defaults as ([]).
    objs: Dict[str, TimedList] = \
        field(init=False,
              default_factory=
              lambda: dict(
                  hits=HitList([]),
                  holds=HoldList([]),
                  bpms=BpmList([]))
              )

    def __getitem__(self, item: Type[T]) -> List[Type[T]]:
        li = [o for o in self.objs.values() if isinstance(o, item)]
        if li:
            return li
        else:
            raise IndexError(f"Object of type {item} does not exist.")

    def __setitem__(self, key: T, value: List[Type[T]]):
        this = self.__getitem__(key)
        assert len(this) == len(
            value), "The lengths of the set and get must be the same."
        for i in range(len(this)):
            # noinspection PyTypeChecker
            this[i] = value[i]

    @property
    def notes(self):
        return self[NoteList]

    # noinspection PyUnresolvedReferences
    @notes.setter
    def notes(self, val):
        for i in range(len(val)):
            self[NoteList][i] = val[i]

    def deepcopy(self) -> Map:
        """Returns a deep copy of itself"""
        return deepcopy(self)

    # @abstractmethod
    def metadata(self, unicode=True, **kwargs) -> str:
        """Grabs the map metadata

        Notes:
            This doesn't try to convert unicode to ascii.
        Args:
            unicode: Whether to use unicode if available.

        Returns:
            A string containing the metadata
        """
        ...

    def describe(self,
                 rounding: int = 2,
                 unicode: bool = False,
                 **kwargs) -> str:
        """Describes the map's attributes as a short summary

        Examples:

            >>> from reamber.base import Hit, Bpm
            >>> bpms = [Bpm(offset=1000, bpm=120)]
            >>> hits = [Hit(offset=1000, column=1),
            ...         Hit(offset=2000, column=2)]
            >>> m = Map()
            >>> m.hits = HitList(hits)
            >>> m.bpms = BpmList(bpms)
            >>> m.describe() # doctest: +ELLIPSIS
            "..."

        Args:
            rounding: The decimal rounding
            unicode: Whether to use unicode if available.
        """

        first = min([nl.first_offset() for nl in self[NoteList] if nl])
        last = max([nl.last_offset() for nl in self[NoteList] if nl])

        out = f"Average BPM: " \
              f"{round(self[BpmList][0].ave_bpm(last), rounding)}\n" \
              f"Map Length: " \
              f"{datetime.timedelta(milliseconds=last - first)}\n" \
              f"{self.metadata(unicode=unicode, **kwargs)} + \n\n" \
              f"--- Notes ---\n"

        for n in self[NoteList]:
            n: TimedList
            out += f"{n.__class__.__name__}\n" \
                   f"{n.df.columns}\n" \
                   f"{n.df.describe()}\n\n"
        return out

    def rate(self, by: float) -> Map:
        """Changes the rate of the map

        Examples:
            The following will uprate the map by 10%

            >>> Map().rate(1.1) # doctest: +ELLIPSIS
            Map(...)

        Args:
            by: The rate.
        """

        copy = self.deepcopy()
        stack = copy.stack()
        stack.offset /= by
        stack.bpm *= by
        stack.length /= by
        return copy

    @stack_props()
    class Stacker:
        """Stacking merges multiple ``TimedList`` to map operations on them.

        The internal data class is a ``pd.DataFrame``.

        Examples:

            >>> from reamber.base import Hit
            >>> hits = [Hit(offset=1000, column=1),
            ...         Hit(offset=2000, column=2)]
            >>> m = Map()
            >>> m.hits = HitList(hits)
            >>> stack = m.stack()

            Multiply all offsets in the map by 2

            >>> stack.offset *= 2
            >>> stack.offset.tolist()
            [2000.0, 4000.0]

            Or if you do it inline,

            >>> m.stack().offset *= 2
            >>> m.hits.offset.tolist()
            [4000.0, 8000.0]

            Notice that ``stack`` changes the map directly by reference.

            If the property, like ``column``, doesn't exist for ``Bpm``,
            it will simply skip it for ``Bpm``.

            However, all properties must exist at least once.

            For example,

            >>> try:
            ...     stack.does_not_exist *= 2
            ... except Excepti  on:
            ...     print("No such property")
            No such property

            The internal data class is a ``pd.DataFrame``:

            >>> hits = [Hit(offset=1000, column=1),
            ...         Hit(offset=2000, column=2),
            ...         Hit(offset=3000, column=3)]
            >>> m = Map()
            >>> m.hits = HitList(hits)
            >>> stack = m.stack()
            >>> stack.offset[stack.column < 2].tolist()
            [1000.0]

            >>> stack.offset[stack.column > 1].tolist()
            [2000.0, 3000.0]

            If you need more conditions, use ``loc``
        """

        """We concat all dfs and do operations on the joined df. 
        However, concat of dfs will always be deep copied.
        Thus, any updates to the concat needs to update the original list 
        
        LISTS ---STACK---> COPY ---> STACKED
          +---------- REFERENCE ---> UNSTACKED  
        
        To do so, we track of the links between unstacked and stacked by ix.
        
        IXS        |         |          |    |     |
        UNSTACKED  [........] [........] [..] [....]
        STACKED    [...............................]
        
        So any operation will affect the stacked, 
        any mutation will call _update, updating unstacked.
        
        """

        _ixs: List[int]
        _unstacked: List[TimedList]

        # This is concat of all lists, making common ops possible.
        _stacked: pd.DataFrame

        def __init__(self, objs: List[TimedList]):
            ixs: List = [0]
            for obj in objs:
                ixs.append(ixs[-1] + len(obj))
            self._ixs = ixs
            self._unstacked = objs
            self._stacked = pd.concat(
                [v.df for v in self._unstacked]
            ).reset_index()

        @property
        def loc(self) -> StackerLocIndexer:
            """Loc is used when basic indexing is insufficient.

            Notes:
                This is similar to how ``pandas`` uses ``loc``.
                You may assume the same syntax.

            Examples:
                >>> from reamber.base import Hit
                >>> hits = [Hit(offset=1000, column=1),
                ...         Hit(offset=2000, column=2),
                ...         Hit(offset=3000, column=3)]
                >>> m = Map()
                >>> m.hits = HitList(hits)
                >>> stack = m.stack()

                >>> stack.loc[stack.offset > 1000, 'column'] += 1
                >>> m.hits.column.tolist()
                [1.0, 3.0, 4.0]

                >>> stack.loc[
                ...     (stack.column == 1) & (stack.offset <= 1000),
                ...     ['offset']
                ... ] *= 2
                >>> m.hits.offset.tolist()
                [2000.0, 2000.0, 3000.0]

            """
            return self.StackerLocIndexer(self._stacked.loc, self)

        def _update(self):
            for obj, ix_i, ix_j in zip(
                self._unstacked, self._ixs[:-1], self._ixs[1:]
            ):
                obj.df = self._stacked[obj.df.columns].iloc[ix_i:ix_j]

        def __getitem__(self, item):
            return self._stacked[item]

        def __setitem__(self, key, value):
            self._stacked[key] = value
            self._update()

        _props = ['offset', 'column', 'length', 'bpm', 'metronome']

        @dataclass
        class StackerLocIndexer:
            """Class generated with ``Stacker.loc``

            Notes:
                See Documentation in ``Stacker.loc`` on usage.
            """
            loc: _LocIndexer
            stacker: Map.Stacker

            def __setitem__(self, key, value):
                self.loc.__setitem__(key, value)
                self.stacker._update()

            def __getitem__(self, item):
                return self.loc.__getitem__(item)

    def stack(self, include_types: Tuple[Type[T]] = None) -> Stacker:
        """Stacks map and includes specific columns

        Examples:
            This will generate a stacker ``stack``

            >>> from reamber.base import Hit
            >>> hits = [Hit(offset=1000, column=1),
            ...         Hit(offset=2000, column=2),
            ...         Hit(offset=3000, column=3)]
            >>> m = Map()
            >>> m.hits = HitList(hits)
            >>> m.stack() # doctest: +ELLIPSIS
            <Map.Map.Stacker ...>

        Returns:
            A ``Map.Stacker`` instance. This is a pass by reference.
            Thus, modifications on the stack will change the map directly.

        """

        if include_types is None:
            objs = [v for v in self.objs.values()]
        else:
            # noinspection PyTypeHints
            objs = [v for v in self.objs.values()
                    if isinstance(v, include_types)]
        return self.Stacker(objs)

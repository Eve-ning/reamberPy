from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, Iterator, TypeVar, Union, Any, Generic

import numpy as np
import pandas as pd

from reamber.base.Map import Map
from reamber.base.Property import stack_props
from reamber.base.lists import TimedList

NoteListT = TypeVar('NoteListT')
HitListT = TypeVar('HitListT')
HoldListT = TypeVar('HoldListT')
BpmListT = TypeVar('BpmListT')
MapT = TypeVar('MapT')


@dataclass
class MapSet(Generic[NoteListT, HitListT, HoldListT, BpmListT, MapT]):

    maps: List[MapT[NoteListT, HitListT, HoldListT, BpmListT]] = field(default_factory=lambda: [])

    def __init__(self, maps: List[MapT[NoteListT, HitListT, HoldListT, BpmListT]]):
        self.maps = maps

    def __iter__(self) -> Iterator[MapT]:
        for m in self.maps:
            yield m

    def items(self):
        for m in self.maps:
            yield m.__class__, m

    def __getitem__(self, item: Union[Any, type]):
        if isinstance(item, type):
            # We want to index by type.
            return [m[item][0] for m in self.maps]
        else:
            # We want to index by slice/int/etc.
            return self.maps[item]

    def __setitem__(self, key: Union[Any, type], value):
        this = self[key]
        assert len(this) == len(value), "The lengths of the set and get must be the same."
        for i in range(len(this)): this[i] = value[i]

    def deepcopy(self):
        """ Returns a deep copy of itself """
        return deepcopy(self)

    def describe(self, rounding: int = 2, unicode: bool = False) -> List[str]:
        """ Describes the map's attributes as a short summary

        :param rounding: The decimal rounding
        :param unicode: Whether to attempt to get the non-unicode or unicode. \
            Doesn't attempt to translate.
        """

        return [m.describe(rounding=rounding, unicode=unicode, s=self) for m in self]

    def rate(self, by: float) -> MapSet:
        """ Changes the rate of the map. Note that you need to do rate on the mapset to affect BPM.

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        """
        copy = self.deepcopy()
        copy.maps = [m.rate(by=by) for m in copy.maps]
        return copy

    # noinspection DuplicatedCode,PyUnresolvedReferences
    @stack_props()
    class Stacker:
        """ This purpose of this class is to provide unnamed access to the lists.

        This can make code much shorter as we don't have to deal with keyed dicts.

        For example,
        >>> m = Map.stack
        >>> m.offset *= 2

        Or if you do it inline,
        >>> m.stack.lengths *= 2

        This will change the offsets of all lists that have the offset property.
        This will change the map itself, as stack is a reference

        This also is a "naive" system, so if the property, like column, doesn't exist
        for Bpms, it will not break it. However, all properties must exist at least
        once.

        If the property isn't listed here, you can do string indexing

        For example,
        >>> m = Map.stack
        >>> m.other_property *= 2

        """

        """ How does this work? 

        Firstly, if you concat a list of dfs, pd will always make a copy, so you have to 
        preserve the original dfs and also the stacked.

        LISTS ---STACK---> COPY ---> STACKED
          +---------- REFERENCE ---> UNSTACKED  

        The reason for stacking is so that we don't have to loop through all dfs to mutate.
        If we did loop through the dfs, we have to stack them anyways, so it's as efficient.
        However, it's just easier, by my eyes, to stack then attempt to mutate.

        So, we keep 2 things in check, the unstacked, and the stacked.

        However, we only can mutate the stacked one, then convert to the unstacked, because
        the unstacked is the referenced.

        Hence, we keep track of what partitions of the unstacked are each of the stacked.

        IXS        |         |          |    |     |
        UNSTACKED  [........] [........] [..] [....]
        STACKED    [...............................]

        That's where ixs come in to help in converting the stacked values to unstacked.

        So the workflow is that when we retrieve a value, it's always from the stacked.
        Then, when it's mutated, it can be set and it will always call the _update
        to update the referenced unstacked.

        """

        stackers: List[Map.Stacker]

        # noinspection PyProtectedMember
        def __init__(self, maps: List[MapT]):
            self.stackers = [m.stack for m in maps]

        def __getitem__(self, item):
            return pd.DataFrame([i[item] for i in self.stackers])

        def __setitem__(self, key, value):
            for s, i in zip(self.stackers, value.iloc):
                s[key] = i

        _props = ['offset', 'column', 'length', 'bpm', 'metronome']

    @property
    def stack(self):
        """ This creates a mutator for this instance, see Mutator for details. """
        return MapSet.Stacker(self.maps)

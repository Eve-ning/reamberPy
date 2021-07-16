from __future__ import annotations

from copy import deepcopy
from typing import List, Dict, Iterator

import numpy as np
import pandas as pd

from reamber.base.Map import Map
from reamber.base.Property import stack_props
from reamber.base.lists import TimedList


class MapSet:

    maps: List[Map]

    def __init__(self, maps: List[Map]):
        self._maps = maps

    def __iter__(self) -> Iterator[Map]:
        for m in self.maps:
            yield m

    def __getitem__(self, item) -> Map:
        return self.maps[item]

    def __setitem__(self, key, value):
        self.maps[key] = value

    @property
    def maps(self):
        return self._maps

    @maps.setter
    def maps(self, val):
        self._maps = val

    @property
    def offsets(self) -> List[Dict[str, TimedList]]:
        return [m.offset for m in self.maps]

    @offsets.setter
    def offsets(self, val: List[Dict[str, TimedList]]):
        for m, v in zip(self.maps, val):
            m.offset = v

    def deepcopy(self):
        """ Returns a deep copy of itself """
        return deepcopy(self)

    def describe(self, rounding: int = 2, unicode: bool = False) -> List[str]:
        """ Describes the map's attributes as a short summary

        :param rounding: The decimal rounding
        :param unicode: Whether to attempt to get the non-unicode or unicode. \
            Doesn't attempt to translate.
        """

        return [m.describe(rounding=rounding, unicode=unicode) for m in self.maps]

    def rate(self, by: float) -> MapSet:
        """ Changes the rate of the map. Note that you need to do rate on the mapset to affect BPM.

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        """

        return MapSet([m.rate(by=by) for m in self.maps])

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

        _ixs: np.ndarray
        _unstacked: List[Dict[str, TimedList]]

        # The stacked property is a concat of all lists, this makes the common ops possible.
        _stacked: pd.DataFrame

        _stacks: List
        def __init__(self, maps: List[Map]):
            stackers = [m.stack for m in maps]
            self._stacked = pd.concat([s._stacked for s in stackers])

            ixs = np.asarray([s._ixs for s in stackers])
            cumulative = np.roll(np.max(ixs, axis=1), shift=1)
            cumulative[0] = 0
            cumulative = np.cumsum(cumulative)
            ixs += cumulative[..., np.newaxis]
            self._ixs = np.unique(np.sort(ixs.flatten()))
            self._unstacked = [m.lists for m in maps]

            assert len(self._ixs) - 1 == sum([len(m.lists) for m in maps]),\
                f"Unexpected length mismatch. ixs: {len(self._ixs) - 1} - 1 " \
                f"!= lists:{sum([len(m.lists) for m in maps])}"

        def _update(self):
            i = 0
            for m in self._unstacked:  # For each map in unstacked
                for k, v in m.items():
                    # For each k: list_name, v: list
                    v.df = self._stacked[self._ixs[i]:self._ixs[i+1]]
                    i += 1

        def __getitem__(self, item):
            return self._stacked[item]

        def __setitem__(self, key, value):
            self._stacked[key] = value
            self._update()

        _props = ['offset', 'column', 'length', 'bpm', 'metronome']

    @property
    def stack(self):
        """ This creates a mutator for this instance, see Mutator for details. """
        return MapSet.Stacker(self.maps)

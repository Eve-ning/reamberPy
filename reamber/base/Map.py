from __future__ import annotations

import datetime
from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, TypeVar, Generic

import pandas as pd

from reamber.base.Property import stack_props
from reamber.base.lists.BpmList import BpmList
from reamber.base.lists.TimedList import TimedList
from reamber.base.lists.notes.NoteList import NoteList

NoteListT = TypeVar('NoteListT')
HitListT = TypeVar('HitListT')
HoldListT = TypeVar('HoldListT')
BpmListT = TypeVar('BpmListT')


@dataclass
class Map(Generic[NoteListT, HitListT, HoldListT, BpmListT]):
    """ This class should be inherited by all Map Objects

    They must inherit the data method, which extracts all data they hold.
    They are also assumed to be a TimedList.
    """

    objects: List[TimedList] = field(default_factory=lambda: [])

    def __getitem__(self, item: type):
        li = [o for o in self.objects if isinstance(o, item)]
        if li: return li
        else: raise IndexError(f"Object of type {item} does not exist.")

    def __setitem__(self, key: type, value: List[TimedList]):
        this = self[key]
        assert len(this) == len(value), "The lengths of the set and get must be the same."
        for i in range(len(this)): this[i] = value[i]

    @property
    def note_list(self) -> List[NoteList]:
        return [o for o in self.objects if isinstance(o, NoteList)]

    def deepcopy(self) -> Map:
        """ Returns a deep copy of itself """
        return deepcopy(self)

    # @abstractmethod
    def metadata(self, unicode=True, **kwargs) -> str:
        """ Grabs the map metadata

        :param unicode: Whether to try to find the unicode or non-unicode. \
            This doesn't try to convert unicode to ascii, it just looks for if there's an available translation.
        :return: A string containing the metadata
        """
        ...

    def describe(self, rounding: int = 2, unicode: bool = False, **kwargs) -> str:
        """ Describes the map's attributes as a short summary

        :param rounding: The decimal rounding
        :param unicode: Whether to attempt to get the non-unicode or unicode. \
            Doesn't attempt to translate.
        """

        first = min([nl.first_offset() for nl in self[NoteList]])
        last = max([nl.last_offset() for nl in self[NoteList]])
        return f"Average BPM: {round(self[BpmList][0].ave_bpm(), rounding)}\n"\
               f"Map Length: {datetime.timedelta(milliseconds=last - first)}"\
               f"{self.metadata(unicode=unicode, **kwargs)}"\
               f"---- NPS ----"\
               f"{[n.describe_notes() for n in self[NoteList]]}"

    def rate(self, by: float) -> Map:
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the duration.
        """

        copy = self.deepcopy()
        s = copy.stack
        s.offset /= by
        s.length /= by
        return copy

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

        _ixs: List[int]
        _unstacked: List[TimedList]

        # The stacked property is a concat of all lists, this makes the common ops possible.
        _stacked: pd.DataFrame

        def __init__(self, objs: List[TimedList]):
            ixs: List = [0]
            for obj in objs:
                ixs.append(ixs[-1] + len(obj))
            self._ixs = ixs
            self._unstacked = objs
            self._stacked = pd.concat([v.df for v in self._unstacked])

        def _update(self):
            for obj, ix_i, ix_j in zip(self._unstacked, self._ixs[:-1], self._ixs[1:]):
                obj.df = self._stacked[obj.df.columns].iloc[ix_i:ix_j]

        def __getitem__(self, item):
            return self._stacked[item]

        def __setitem__(self, key, value):
            self._stacked[key] = value
            self._update()

        _props = ['offset', 'column', 'length', 'bpm', 'metronome']

    @property
    def stack(self):
        """ This creates a mutator for this instance, see Mutator for details. """
        return Map.Stacker(self.objects)

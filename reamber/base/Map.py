from __future__ import annotations

import datetime
from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, TypeVar, Generic, Dict

import pandas as pd
from pandas.core.indexing import _LocIndexer

from reamber.base.Property import stack_props, map_props
from reamber.base.lists.BpmList import BpmList
from reamber.base.lists.TimedList import TimedList
from reamber.base.lists.notes.HitList import HitList
from reamber.base.lists.notes.HoldList import HoldList
from reamber.base.lists.notes.NoteList import NoteList

NoteListT = TypeVar('NoteListT')
HitListT = TypeVar('HitListT')
HoldListT = TypeVar('HoldListT')
BpmListT = TypeVar('BpmListT')


@dataclass
@map_props()
class Map(Generic[NoteListT, HitListT, HoldListT, BpmListT]):
    """ This class should be inherited by all Map Objects

    They must inherit the data method, which extracts all data they hold.
    They are also assumed to be a TimedList.
    """

    _props = dict(hits=HitList, holds=HoldList, bpms=BpmList)

    """objs is the objects of the class, it MUST be defined, and must have defaults as ([]). """
    objs: Dict[str, TimedList] = \
        field(init=False,
              default_factory=lambda: dict(hits=HitList([]), holds=HoldList([]), bpms=BpmList([])))

    def __getitem__(self, item: type):
        li = [o for o in self.objs.values() if isinstance(o, item)]
        if li: return li
        else: raise IndexError(f"Object of type {item} does not exist.")

    def __setitem__(self, key: type, value: List[TimedList]):
        this = self.__getitem__(key)
        assert len(this) == len(value), "The lengths of the set and get must be the same."
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

    def describe(self, rounding: int = 2, **kwargs) -> str:
        """ Describes the map's attributes as a short summary

        :param rounding: The decimal rounding
        """

        first = min([nl.first_offset() for nl in self[NoteList] if nl])
        last = max([nl.last_offset() for nl in self[NoteList] if nl])
        out = f"Average BPM: {round(self[BpmList][0].ave_bpm(last), rounding)}\n"
        out += f"Map Length: {datetime.timedelta(milliseconds=last - first)}\n"
        out += self.metadata(**kwargs) + "\n\n"
        out += "--- Notes ---\n"
        for n in self[NoteList]:
            n: TimedList
            out += n.__class__.__name__ + '\n'
            out += str(n.df.columns) + '\n'
            out += str(n.df.describe()) + '\n\n'
        return out

    def rate(self, by: float) -> Map:
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the duration.
        """

        copy = self.deepcopy()
        s = copy.stack()
        s.offset /= by
        s.bpm *= by
        s.length /= by
        return copy

    # noinspection PyUnresolvedReferences
    @stack_props()
    class Stacker:
        """ This purpose of this class is to provide unnamed access to the lists.

        This can make code much shorter as we don't have to deal with keyed dicts.

        For example,

        >>> m = Map.stack()
        >>> m.offset *= 2

        Or if you do it inline,

        >>> m.stack().lengths *= 2

        This will change the offsets of all lists that have the offset property.
        This will change the map itself, as stack is a reference

        This also is a "naive" system, so if the property, like column, doesn't exist
        for Bpms, it will not break it. However, all properties must exist at least
        once.

        If the property isn't listed here, you can do string indexing

        For example,

        >>> m = Map.stack()
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
            self._stacked = pd.concat([v.df for v in self._unstacked]).reset_index()

        @property
        def loc(self):
            return self.StackerLocIndexer(self._stacked.loc, self)

        def _update(self):
            for obj, ix_i, ix_j in zip(self._unstacked, self._ixs[:-1], self._ixs[1:]):
                obj.df = self._stacked[obj.df.columns].iloc[ix_i:ix_j]

        def __getitem__(self, item):
            return self._stacked[item]

        def __setitem__(self, key, value):
            self._stacked[key] = value
            self._update()

        _props = ['offset', 'column', 'length', 'bpm', 'metronome']

        @dataclass
        class StackerLocIndexer:
            loc: _LocIndexer
            stacker: Map.Stacker

            def __setitem__(self, key, value):
                self.loc.__setitem__(key, value)
                self.stacker._update()

            def __getitem__(self, item):
                return self.loc.__getitem__(item)

    def stack(self, include:List[str] = None) -> Stacker:
        """ This creates a mutator for this instance, see Mutator for details. """
        assert isinstance(include, list) or include is None, "The input must be a list."

        return self.Stacker([v for k, v in list(self.objs.items()) if k in include]
                            if include
                            else list(self.objs.values()))

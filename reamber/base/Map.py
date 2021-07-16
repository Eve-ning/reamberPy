from __future__ import annotations

import datetime
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, List, TypeVar, Generic

import pandas as pd

from reamber.base.Property import stack_props
from reamber.base.lists.BpmList import BpmList
from reamber.base.lists.NotePkg import NotePkg
from reamber.base.lists.TimedList import TimedList
from reamber.base.lists.notes.HitList import HitList
from reamber.base.lists.notes.HoldList import HoldList

HitListT = TypeVar('HitListT')
HoldListT = TypeVar('HoldListT')
BpmListT = TypeVar('BpmListT')
NotePkgT = TypeVar('NotePkgT', bound=NotePkg)


@dataclass
class Map(Generic[HitListT, HoldListT, NotePkgT, BpmListT]):
    """ This class should be inherited by all Map Objects

    They must inherit the data method, which extracts all data they hold.
    They are also assumed to be a TimedList.
    """

    notes: NotePkg = field(default_factory=lambda: NotePkg(hits=HitList([]), holds=HoldList([])))
    bpms: BpmList = field(default_factory=lambda: BpmList([]))

    @property
    def lists(self) -> Dict[str, TimedList]:
        return {**self.notes.lists, 'bpms': self.bpms}

    def __getitem__(self, item) -> TimedList:
        return self.lists[item]

    def __setitem__(self, key: str, value: TimedList):
        self.lists[key] = value

    @property
    def offset(self):
        return {k: v.offset for k, v in self.lists.items()}

    @offset.setter
    def offset(self, val: Dict[str, TimedList]):
        for k, v in val.items():
            self.lists[k] = val[k]

    def deepcopy(self) -> Map:
        """ Returns a deep copy of itself """
        return deepcopy(self)

    def ave_bpm(self, last_offset: float = None) -> float:
        """ Calculates the average Bpm.

        :param last_offset: If not None, then this offset will be used to terminate activity,
            else last note offset will be used.
        """

        return self.bpms.ave_bpm(last_offset if last_offset else self.notes.last_offset())

    def scroll_speed(self, reference_bpm: float = None) -> List[Dict[str, float]]:
        """ Evaluates the scroll speed based on mapType

        e.g. if BPM == 200.0 and CenterBPM == 100.0, it'll return {'offset': X, 'speed': 2.0}

        :param reference_bpm: The bpms to zero calculations on. If None, it'll just be the multiplication of bpms and sv.
        :return: Returns a list dict of keys offset and speed
        """

        # This automatically calculates the center BPM
        # Bpm Activity implicitly sorts
        if reference_bpm is None: reference_bpm = 1
        return [dict(offset=bpm.offset, speed=bpm.bpm / reference_bpm) for bpm in self.bpms]

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

        first, last = self.notes.first_last_offset()
        return f"Average BPM: {round(self.ave_bpm(), rounding)}\n"\
               f"Map Length: {datetime.timedelta(milliseconds=last - first)}"\
               f"{self.metadata(unicode=unicode, **kwargs)}"\
               f"---- NPS ----"\
               f"{self.notes.describe_notes()}"

    def rate(self, by: float) -> Map:
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        """

        copy = self.deepcopy()
        for k, v in copy.offset.items():
            v /= by
        copy.notes.holds.length /= by
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
        _unstacked: Dict[str, TimedList]

        # The stacked property is a concat of all lists, this makes the common ops possible.
        _stacked: pd.DataFrame

        def __init__(self, lists: Dict[str, TimedList]):
            ixs: List = [0]
            for k, v in lists.items():
                ixs.append(ixs[-1] + len(v))
            self._ixs = ixs
            self._unstacked = lists
            self._stacked = pd.concat([v.df for v in self._unstacked.values()])

        def _update(self):
            for (k, v), ix_i, ix_j in zip(self._unstacked.items(), self._ixs[:-1], self._ixs[1:]):
                v.df = self._stacked[v.df.columns].iloc[ix_i:ix_j]

        def __getitem__(self, item):
            return self._stacked[item]

        def __setitem__(self, key, value):
            self._stacked[key] = value
            self._update()

        _props = ['offset', 'column', 'length', 'bpm', 'metronome']

    @property
    def stack(self):
        """ This creates a mutator for this instance, see Mutator for details. """
        return Map.Stacker(self.lists)

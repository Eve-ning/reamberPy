from __future__ import annotations

import datetime
from copy import deepcopy
from typing import Dict, List

import pandas as pd

from reamber.base.lists.BpmList import BpmList
from reamber.base.lists.NotePkg import NotePkg
from reamber.base.lists.TimedList import TimedList


class Map:
    """ This class should be inherited by all Map Objects

    They must inherit the data method, which extracts all data they hold.
    They are also assumed to be a TimedList.
    """

    def __init__(self, notes: NotePkg, bpms: BpmList):
        self._notes = notes
        self._bpms = bpms

    @property
    def notes(self) -> NotePkg: ...
    @notes.setter
    def notes(self, val): ...
    @property
    def bpms(self) -> BpmList: ...
    @bpms.setter
    def bpms(self, val): ...
    @property
    def lists(self) -> Dict[str, TimedList]: ...
    def __getitem__(self, item) -> TimedList: ...
    def __setitem__(self, key: str, value: TimedList): ...
    @property
    def offset(self): ...
    @offset.setter
    def offset(self, val: Dict[str, TimedList]): ...
    def deepcopy(self) -> Map: ...
    def ave_bpm(self, last_offset: float = None) -> float: ...
    def scroll_speed(self, reference_bpm: float = None) -> List[Dict[str, float]]: ...
    def metadata(self, unicode=True, **kwargs) -> str: ...
    def describe(self, rounding: int = 2, unicode: bool = False, **kwargs) -> str: ...
    def rate(self, by: float) -> Map: ...
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

        def __init__(self, lists: Dict[str, TimedList]): ...
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
    def stack(self) -> Stacker: ...

from __future__ import annotations

from typing import List, overload, Any, Union

import numpy as np
import pandas as pd

from reamber.algorithms.timing import TimingMap, BpmChangeOffset
from reamber.base import Bpm
from reamber.base import RAConst
from reamber.base.lists.TimedList import TimedList


class BpmList(TimedList[Bpm]):
    """ A List that holds a list of Bpms, useful to do group Bpm operations """

    def __init__(self, objs: Union[List[Bpm], Bpm, pd.DataFrame]):
        super(BpmList, self).__init__(objs=objs)

    @property
    def _init_empty(self) -> dict:
        """ Initializes the DataFrame if no objects are passed to init. """
        return dict(**super(BpmList, self)._init_empty,
                    bpm=pd.Series([], dtype='float'),
                    metronome=pd.Series([], dtype='float'))

    @property
    def _item_class(self) -> type:
        """ This is the class type for a singular item, this is needed for correct casting when indexing. """
        return Bpm

    # This is required so that the typing returns are correct.
    @overload
    def __getitem__(self, item: slice) -> BpmList: ...
    @overload
    def __getitem__(self, item: list) -> BpmList: ...
    @overload
    def __getitem__(self, item: Any) -> BpmList: ...
    @overload
    def __getitem__(self, item: int) -> Bpm: ...
    def __getitem__(self, item):
        # This is an interesting way to use the callee class
        # e.g., if the subclass, Note, calls this, it'll be Note(self.df[item]).
        # self(self.df[item]) doesn't work as self is an instance.

        if isinstance(item, int):
            return self._item_class(**self.df.iloc[item].to_dict())
        else:
            return self.__class__(self.df[item])

    @property
    def bpms(self) -> pd.Series:
        return self.df['bpm']

    @bpms.setter
    def bpms(self, val):
        self.df['bpm'] = val

    @property
    def metronomes(self):
        return self.df['metronome']

    @metronomes.setter
    def metronomes(self, val):
        self.df['metronome'] = val

    def snap_offsets(self, nths: float = 1.0,
                     last_offset: float = None) -> np.ndarray:
        """ Gets all of the nth snap offsets

        For example::

            SEC     1   2   3   4   5   6   7   8   9   10  11  12  13  14  ...
            BPM     15                          7.5                         ...
            SNAP    4/4 1/4 2/4 3/4 4/4 1/4 2/4 4/4 1/8 2/8 3/8 4/8 5/8 6/8 ...
            BEAT    1               2           3
            nths=1  ^               ^           ^
            nths=2  ^       ^       ^       ^   ^               ^
            nths=4  ^   ^   ^   ^   ^   ^   ^   ^       ^       ^       ^
            nths=8  ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^   ^   ^   ^   ^   ^   ^

        * Note: 15 BPM = 1 Beat per 4 seconds, 7.5 = 1 Beat per 8 seconds

        The `^` indicates what offsets will be returned.

        :param nths: Specifies the beat's snap, 1 = "1st"s, 4 = "4th"s, 16 = "16th"s
        :param last_offset: The last offset to consider, if None, it uses the last BPM
        """
        self_ = self.deepcopy()
        if last_offset: self_.append(Bpm(last_offset, bpm=0))  # BPM doesn't matter for the last.

        offsets = []
        for i, j in zip(self[:-1], self[1:]):
            i: Bpm
            j: Bpm
            offset_diff = j.offset - i.offset
            nth_diff = i.beat_length / nths
            offsets.append(np.arange(0, offset_diff, nth_diff) + i.offset)
        return np.concatenate(offsets)

    def to_timing_map(self):
        return TimingMap.time_by_offset(
            initial_offset=self.first_offset(),
            bpm_changes_offset=[BpmChangeOffset(b.bpm, b.metronome, b.offset) for b in self]
        )

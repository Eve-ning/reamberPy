from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
from typing import Tuple, List, Dict, Iterator, TypeVar, Generic

import pandas as pd

NoteListT = TypeVar('NoteListT')
HitListT = TypeVar('HitListT')
HoldListT = TypeVar('HoldListT')

class NotePkg(Generic[NoteListT, HitListT, HoldListT]):
    """ This Package holds multiple note lists """

    _lists = Dict[str, NoteListT]

    def __init__(self, **kwargs: NoteListT):
        """ By default, we have hits and holds for every VSRG.
        This assumption is made so that it's easier to subclass

        The convention is that all VSRGs have a hit and hold type, hence the hits and holds property.

        :param data: A Dictionary of the Note Lists
        """
        self._lists = kwargs

    @property
    def lists(self) -> Dict[str, NoteListT]:
        return self._lists

    @lists.setter
    def lists(self, val):
        self._lists = val

    @property
    def hits(self) -> HitListT:
        return self.lists['hits']

    @property
    def holds(self) -> HoldListT:
        return self.lists['holds']

    def __getitem__(self, item):
        return self._lists[item]

    def __setitem__(self, key, value):
        self._lists[key] = value

    def __len__(self):
        return len(self.lists)

    def __iter__(self) -> Iterator[NoteListT]:
        for li in self.lists:
            yield li

    @property
    def offset(self):
        return {k: li.offset for k, li in self.lists.items()}

    @offset.setter
    def offset(self, vals: Dict):
        for k in self.lists.keys():
            self.lists[k].offset = vals[k]

    @property
    def column(self):
        return {k: li.column for k, li in self.lists.items()}

    @column.setter
    def column(self, vals: Dict):
        for k in self.lists.keys():
            self.lists[k].column = vals[k]

    def deepcopy(self) -> NotePkg:
        """ Creates a deep copy of itself """
        return deepcopy(self)

    def obj_count(self) -> int:
        """ Returns the total sum number of items in each list. For number of lists use len() """
        return sum([len(data) for data in self.lists.values()])

    def in_columns(self, columns: List[int]) -> NotePkg:
        """ Filters by columns for all items

        :param columns: The columns to filter by, as a list
        :return:
        """
        return self.__class__(**{k: v.in_columns(columns) for k, v in self.lists.items()})

    def max_column(self) -> int:
        """ Gets the maximum column, can be used to determine Key Count if not explicitly stated """
        return max([li.max_column() for li in self.lists.values()])

    def first_offset(self) -> float:
        """ Gets the minimum offset """
        i = [li.first_offset() for li in self.lists.values()]
        return min(i) if i else 0

    def last_offset(self) -> float:
        """ Gets the maximum offset """
        i = [li.last_offset() for li in self.lists.values()]
        return max(i) if i else float('inf')

    def first_last_offset(self) -> Tuple[float, float]:
        """ Gets the minimum and maximum offset found """
        return self.first_offset(), self.last_offset()

    def describe_notes(self) -> Dict[str, pd.DataFrame]:
        """ Calls all describes in the list """

        return {k: li.describe() for k, li in self.lists.items()}

    def rolling_density(self, window: int = 1000, stride: int = None,
                        first_offset: float = None, last_offset: float = None) -> Dict[str, Dict[int, int]]:
        """ Returns the Density List Dictionary

        First offset and last offset is recalculated here in Package to make sure that the indexes are consistent.

        :param window: The window to search in milliseconds.
        :param stride: The stride length of each search in milliseconds, if None, stride = window
        :param first_offset: The first offset to start search on. If None, first_offset will be used.
        :param last_offset: The last offset to end search on. If None, last_offset will be used. \
            (The search will intentionally exceed if it doesn't fit.)
        :return: Dictionary of offset as key and count as value
        """
        return self.method('rolling_density', window=window, stride=stride,
                           first_offset=first_offset if first_offset else self.first_offset(),
                           last_offset=last_offset if last_offset else self.last_offset())

    def duration(self):
        """ Maximum - Minimum offset. """
        return self.last_offset() - self.first_offset()


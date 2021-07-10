from __future__ import annotations

from typing import List, TYPE_CHECKING, Union, overload, Any, TypeVar

import numpy as np
import pandas as pd

from reamber.base import Note
from reamber.base.lists.TimedList import TimedList


class NoteList(TimedList):
    """ Extends from the TimedList to give more base functions to Notes """

    def __init__(self, objs: Union[List[Note], Note, pd.DataFrame]):
        super(NoteList, self).__init__(objs=objs)

    @property
    def _init_empty(self) -> dict:
        """ Initializes the DataFrame if no objects are passed to init. """
        return dict(**super(NoteList, self)._init_empty,
                    column=pd.Series([], dtype='int'))

    @property
    def _item_class(self) -> type:
        return Note

    @overload
    def __getitem__(self, item: slice) -> NoteList: ...
    @overload
    def __getitem__(self, item: list) -> NoteList: ...
    @overload
    def __getitem__(self, item: Any) -> NoteList: ...
    @overload
    def __getitem__(self, item: int) -> Note: ...
    def __getitem__(self, item):
        # noinspection PyTypeChecker
        return super(NoteList, self).__getitem__(item)

    def max_column(self) -> int:
        """ Maximum Column """
        return max(self.columns) if len(self.columns) != 0 else 0

    @property
    def columns(self) -> Union[pd.Series, Any]:
        # The return type is Any to prevent Type Checking during comparison
        return self.df['column']

    @columns.setter
    def columns(self, val):
        self.df['column'] = val

    def in_columns(self, columns: List[int]) -> NoteList:
        """ Gets all objects that are in these columns. This is a deep copy. """
        return self[self.columns.isin(columns)]



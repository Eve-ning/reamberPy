from __future__ import annotations

from typing import List, Union, Any, TypeVar

import pandas as pd

from reamber.base.lists.TimedList import TimedList


Item = TypeVar('Item')

class NoteList(TimedList[Item]):
    """ Extends from the TimedList to give more base functions to Notes """

    @property
    def _init_empty(self) -> dict:
        """ Initializes the DataFrame if no objects are passed to init. """
        return dict(**super(NoteList, self)._init_empty,
                    column=pd.Series([], dtype='int'))

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



from __future__ import annotations

from typing import List, TypeVar

from reamber.base.Note import Note
from reamber.base.Property import list_props
from reamber.base.lists.TimedList import TimedList


Item = TypeVar('Item')

@list_props(Note)
class NoteList(TimedList[Item]):
    """ Extends from the TimedList to give more base functions to Notes """

    def max_column(self) -> int:
        """ Maximum Column """
        return max(self.column) if len(self.column) != 0 else 0

    def in_columns(self, columns: List[int]) -> NoteList:
        """ Gets all objects that are in these columns. This is a deep copy. """
        return self[self.column.isin(columns)]

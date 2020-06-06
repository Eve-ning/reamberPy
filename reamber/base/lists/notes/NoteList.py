from __future__ import annotations

from typing import List, Type, TYPE_CHECKING
from abc import ABC, abstractmethod

from reamber.base.lists.TimedList import TimedList

if TYPE_CHECKING:
    from reamber.base.NoteObject import NoteObject


class NoteList(TimedList, ABC):
    """ Extends from the TimedList to give more base functions to NoteObjects
    """

    @abstractmethod
    def data(self) -> List[Type[NoteObject]]: pass

    def maxColumn(self) -> int:
        """ CALCULATES the key of the map
        Note that keys of the map isn't stored, it's dynamic and not a stored parameter.
        The function just finds the maximum column.
        """
        return max(self.columns())

    def columns(self) -> List[int]:
        return self.attributes('column')

    def inColumns(self, columns: List[int], inplace: bool = False) -> NoteList or None:
        """ Gets all objects that are in these columns """
        if inplace: self.__init__([obj for obj in self.data() if obj.column in columns])
        else: return self._upcast([obj for obj in self.data() if obj.column in columns])

from __future__ import annotations

from typing import List, Type, TYPE_CHECKING
from abc import ABC, abstractmethod

from reamber.base.lists.TimedList import TimedList

if TYPE_CHECKING:
    from reamber.base.NoteObj import NoteObj


class NoteList(TimedList, ABC):
    """ Extends from the TimedList to give more base functions to NoteObjs
    """

    @abstractmethod
    def data(self) -> List[Type[NoteObj]]: pass

    def maxColumn(self) -> int:
        """ CALCULATES the key of the map
        Note that keys of the map isn't stored, it's dynamic and not a stored parameter.
        The function just finds the maximum column.
        """
        if len(self.columns()) == 0: return 0
        return max(self.columns())

    def columns(self) -> List[int]:
        return self.attribute('column')

    def inColumns(self, columns: List[int], inplace: bool = False) -> NoteList or None:
        """ Gets all objects that are in these columns """
        if inplace: self.__init__([obj for obj in self.data() if obj.column in columns])
        else: return self._upcast([obj for obj in self.data() if obj.column in columns])

from __future__ import annotations

from typing import List, Type, TYPE_CHECKING
from abc import ABC, abstractmethod

from reamber.base.lists.TimedList import TimedList
import numpy as np

if TYPE_CHECKING:
    from reamber.base.Note import Note


class NoteList(TimedList, ABC):
    """ Extends from the TimedList to give more base functions to Notes
    """

    @abstractmethod
    def data(self) -> List[Type[Note]]: pass

    def maxColumn(self) -> int:
        """ CALCULATES the key of the map
        Note that keys of the map isn't stored, it's dynamic and not a stored parameter.
        The function just finds the maximum column.
        """
        if len(self.columns()) == 0: return 0
        return max(self.columns())

    def columns(self) -> List[int]:
        return self.attribute('column')

    def inColumns(self, columns: List[int], inplace: bool = False) -> NoteList:
        """ Gets all objects that are in these columns """
        if inplace: self.__init__([obj for obj in self.data() if obj.column in columns])
        else: return self._upcast([obj for obj in self.data() if obj.column in columns])

    def describeNotes(self, rounding: int = 2):
        """ Describes a single NotePkg

        Prints out Count, Median, 75% quantile and max

        :param rounding: The decimal rounding
        """
        # This is fixed to be 1 second for consistency in value
        density = self.rollingDensity(window=1000)
        if len(density.values()) == 0:
            print("No Info")
            return
        print(       f"Count: {len(self)}, "
              f"50% (Median): {float(np.quantile(list(density.values()), 0.5)):.{rounding}f}, "
                       f"75%: {float(np.quantile(list(density.values()),0.75)):.{rounding}f}, "
                f"100% (Max): {float(max(density.values())):.{rounding}f}")


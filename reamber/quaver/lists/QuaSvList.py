from __future__ import annotations

from typing import List

from reamber.base.lists.TimedList import TimedList
from reamber.quaver.QuaSv import QuaSv


class QuaSvList(List[QuaSv], TimedList):

    def _upcast(self, objList: List = None) -> QuaSvList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: QuaSvList
        """
        return QuaSvList(objList)

    def data(self) -> List[QuaSv]:
        return self

    def multipliers(self) -> List[float]:
        return self.attribute('multiplier')

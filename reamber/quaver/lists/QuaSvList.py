from __future__ import annotations
from reamber.base.lists.TimedList import TimedList
from reamber.quaver.QuaSvObj import QuaSvObj
from typing import List


class QuaSvList(List[QuaSvObj], TimedList):

    def _upcast(self, objList: List = None) -> QuaSvList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: QuaSvList
        """
        return QuaSvList(objList)

    def data(self) -> List[QuaSvObj]:
        return self

    def multipliers(self) -> List[float]:
        return self.attribute('multiplier')

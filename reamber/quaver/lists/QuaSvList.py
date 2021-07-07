from __future__ import annotations

from typing import List

from reamber.base.lists.TimedList import TimedList
from reamber.quaver.QuaSv import QuaSv


class QuaSvList(List[QuaSv], TimedList):

    def _upcast(self, obj_list: List = None) -> QuaSvList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: QuaSvList
        """
        return QuaSvList(obj_list)

    def data(self) -> List[QuaSv]:
        return self

    def multipliers(self) -> List[float]:
        return self.attribute('multiplier')

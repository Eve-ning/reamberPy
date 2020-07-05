from __future__ import annotations
from reamber.base.lists.TimedList import TimedList
from reamber.dummy.DmSv import DmSv
from typing import List


class DmSvList(List[DmSv], TimedList):

    def _upcast(self, objList: List = None) -> DmSvList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: DmSvList
        """
        return DmSvList(objList)

    def data(self) -> List[DmSv]:
        return self

    def multipliers(self) -> List[float]:
        """ Gets all Scroll Velocity values """
        return self.attribute('multiplier')

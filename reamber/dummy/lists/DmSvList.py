from __future__ import annotations

from typing import List

from reamber.base.lists.TimedList import TimedList
from reamber.dummy.DmSv import DmSv


class DmSvList(List[DmSv], TimedList):

    def _upcast(self, obj_list: List = None) -> DmSvList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: DmSvList
        """
        return DmSvList(obj_list)

    def data(self) -> List[DmSv]:
        return self

    def multipliers(self) -> List[float]:
        """ Gets all Scroll Velocity values """
        return self.attribute('multiplier')

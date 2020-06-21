from __future__ import annotations
from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSvObj import OsuSvObj
from typing import List


class OsuSvList(List[OsuSvObj], TimedList):

    def _upcast(self, objList: List = None) -> OsuSvList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: OsuSvList
        """
        return OsuSvList(objList)

    def data(self) -> List[OsuSvObj]:
        return self

    def multipliers(self) -> List[float]:
        """ Gets all Scroll Velocity values """
        return self.attribute('multiplier')

from __future__ import annotations

from typing import List

from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSv import OsuSv


class OsuSvList(List[OsuSv], TimedList):

    def _upcast(self, objList: List = None) -> OsuSvList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: OsuSvList
        """
        return OsuSvList(objList)

    def data(self) -> List[OsuSv]:
        return self

    def multipliers(self) -> List[float]:
        """ Gets all Scroll Velocity values """
        return self.attribute('multiplier')

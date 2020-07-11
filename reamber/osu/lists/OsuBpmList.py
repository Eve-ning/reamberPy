from __future__ import annotations

from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.osu.OsuBpm import OsuBpm


class OsuBpmList(BpmList):

    def _upcast(self, objList: List = None) -> OsuBpmList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: OsuBpmList
        """
        return OsuBpmList(objList)

    def data(self) -> List[OsuBpm]:
        return self

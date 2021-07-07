from __future__ import annotations

from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.osu.OsuBpm import OsuBpm


class OsuBpmList(BpmList):

    def _upcast(self, obj_list: List = None) -> OsuBpmList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: OsuBpmList
        """
        return OsuBpmList(obj_list)

    def data(self) -> List[OsuBpm]:
        return self

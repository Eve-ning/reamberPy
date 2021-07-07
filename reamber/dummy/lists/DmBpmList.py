from __future__ import annotations

from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.dummy.DmBpm import DmBpm


class DmBpmList(BpmList):

    def _upcast(self, obj_list: List = None) -> DmBpmList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: DmBpmList
        """
        return DmBpmList(obj_list)

    def data(self) -> List[DmBpm]:
        return self

from __future__ import annotations

from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.bms.BMSBpm import BMSBpm


class BMSBpmList(BpmList):

    def _upcast(self, obj_list: List = None) -> BMSBpmList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: BMSBpmList
        """
        return BMSBpmList(obj_list)

    def data(self) -> List[BMSBpm]:
        return self

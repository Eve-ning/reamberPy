from __future__ import annotations

from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.bms.BMSBpm import BMSBpm


class BMSBpmList(BpmList):

    def _upcast(self, objList: List = None) -> BMSBpmList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: BMSBpmList
        """
        return BMSBpmList(objList)

    def data(self) -> List[BMSBpm]:
        return self

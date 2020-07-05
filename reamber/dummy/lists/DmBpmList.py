from __future__ import annotations
from typing import List
from reamber.base.lists.BpmList import BpmList
from reamber.dummy.DmBpm import DmBpm


class DmBpmList(BpmList):

    def _upcast(self, objList: List = None) -> DmBpmList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: DmBpmList
        """
        return DmBpmList(objList)

    def data(self) -> List[DmBpm]:
        return self

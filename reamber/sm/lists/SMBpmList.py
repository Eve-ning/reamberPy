from __future__ import annotations
from typing import List
from reamber.base.lists.BpmList import BpmList
from reamber.sm.SMBpm import SMBpm


class SMBpmList(BpmList):

    def _upcast(self, objList: List = None) -> SMBpmList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMBpmList
        """
        return SMBpmList(objList)

    def data(self) -> List[SMBpm]:
        return self

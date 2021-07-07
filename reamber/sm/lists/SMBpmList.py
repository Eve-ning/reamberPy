from __future__ import annotations

from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.sm.SMBpm import SMBpm


class SMBpmList(BpmList):

    def _upcast(self, obj_list: List = None) -> SMBpmList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: SMBpmList
        """
        return SMBpmList(obj_list)

    def data(self) -> List[SMBpm]:
        return self

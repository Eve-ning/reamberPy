from __future__ import annotations

from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.o2jam.O2JBpm import O2JBpm


class O2JBpmList(BpmList):

    def _upcast(self, obj_list: List = None) -> O2JBpmList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: O2JBpmList
        """
        return O2JBpmList(obj_list)

    def data(self) -> List[O2JBpm]:
        return self

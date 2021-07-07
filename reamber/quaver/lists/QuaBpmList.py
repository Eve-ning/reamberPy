from __future__ import annotations

from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.quaver.QuaBpm import QuaBpm


class QuaBpmList(BpmList):

    def _upcast(self, obj_list: List = None) -> QuaBpmList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: QuaBpmList
        """
        return QuaBpmList(obj_list)

    def data(self) -> List[QuaBpm]:
        return self

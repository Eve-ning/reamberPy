from __future__ import annotations

from typing import List

from reamber.base.lists.notes.HoldList import HoldList
from reamber.quaver.QuaHold import QuaHold
from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList


class QuaHoldList(List[QuaHold], HoldList, QuaNoteList):

    def _upcast(self, obj_list: List = None) -> QuaHoldList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: QuaHoldList
        """
        return QuaHoldList(obj_list)

    def data(self) -> List[QuaHold]:
        return self

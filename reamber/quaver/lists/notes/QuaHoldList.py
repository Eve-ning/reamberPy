from __future__ import annotations
from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList
from reamber.quaver.QuaHoldObj import QuaHoldObj
from reamber.base.lists.notes.HoldList import HoldList
from typing import List


class QuaHoldList(List[QuaHoldObj], QuaNoteList, HoldList):

    def _upcast(self, objList: List = None) -> QuaHoldList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: QuaHoldList
        """
        return QuaHoldList(objList)

    def data(self) -> List[QuaHoldObj]:
        return self

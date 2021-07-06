from __future__ import annotations

from typing import List

from reamber.base.lists.notes.HoldList import HoldList
from reamber.quaver.QuaHold import QuaHold
from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList


class QuaHoldList(List[QuaHold], HoldList, QuaNoteList):

    def _upcast(self, objList: List = None) -> QuaHoldList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: QuaHoldList
        """
        return QuaHoldList(objList)

    def mult_offset(self, by: float, inplace:bool = False):
        HoldList.mult_offset(self, by=by, inplace=inplace)

    def data(self) -> List[QuaHold]:
        return self

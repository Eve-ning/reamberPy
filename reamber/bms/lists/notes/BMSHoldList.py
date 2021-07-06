from __future__ import annotations

from typing import List

from reamber.base.lists.notes.HoldList import HoldList
from reamber.bms.BMSHold import BMSHold
from reamber.bms.lists.notes.BMSNoteList import BMSNoteList


class BMSHoldList(List[BMSHold], HoldList, BMSNoteList):

    def _upcast(self, objList: List = None) -> BMSHoldList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: BMSHoldList
        """
        return BMSHoldList(objList)

    def mult_offset(self, by: float, inplace:bool = False):
        HoldList.mult_offset(self, by=by, inplace=inplace)

    def data(self) -> List[BMSHold]:
        return self


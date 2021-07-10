from __future__ import annotations

from typing import List

from reamber.base.lists.notes.HoldList import HoldList
from reamber.bms.BMSHold import BMSHold
from reamber.bms.lists.notes.BMSNoteList import BMSNoteList


class BMSHoldList(List[BMSHold], HoldList, BMSNoteList):

    def _upcast(self, obj_list: List = None) -> BMSHoldList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: BMSHoldList
        """
        return BMSHoldList(obj_list)

    def data(self) -> List[BMSHold]:
        return self


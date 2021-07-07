from __future__ import annotations

from typing import List

from reamber.base.lists.notes.HoldList import HoldList
from reamber.dummy.DmHold import DmHold
from reamber.dummy.lists.notes.DmNoteList import DmNoteList


class DmHoldList(List[DmHold], HoldList, DmNoteList):

    def _upcast(self, obj_list: List = None) -> DmHoldList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: DmHoldList
        """
        return DmHoldList(obj_list)

    def mult_offset(self, by: float, inplace:bool = False):
        HoldList.mult_offset(self, by=by, inplace=inplace)

    def data(self) -> List[DmHold]:
        return self


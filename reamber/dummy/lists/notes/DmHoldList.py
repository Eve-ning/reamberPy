from __future__ import annotations
from reamber.dummy.lists.notes.DmNoteList import DmNoteList
from reamber.dummy.DmHold import DmHold
from reamber.base.lists.notes.HoldList import HoldList
from typing import List


class DmHoldList(List[DmHold], HoldList, DmNoteList):

    def _upcast(self, objList: List = None) -> DmHoldList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: DmHoldList
        """
        return DmHoldList(objList)

    def multOffset(self, by: float, inplace:bool = False):
        HoldList.multOffset(self, by=by, inplace=inplace)

    def data(self) -> List[DmHold]:
        return self


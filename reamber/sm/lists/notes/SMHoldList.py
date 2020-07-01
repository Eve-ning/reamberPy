from __future__ import annotations
from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMHold import SMHold
from reamber.base.lists.notes.HoldList import HoldList
from typing import List


class SMHoldList(List[SMHold], HoldList, SMNoteList):

    def _upcast(self, objList: List = None) -> SMHoldList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMHoldList
        """
        return SMHoldList(objList)

    def multOffset(self, by: float, inplace:bool = False):
        HoldList.multOffset(self, by=by, inplace=inplace)

    def data(self) -> List[SMHold]:
        return self

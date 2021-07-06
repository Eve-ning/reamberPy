from __future__ import annotations

from typing import List

from reamber.base.lists.notes.HoldList import HoldList
from reamber.sm.SMHold import SMHold
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMHoldList(List[SMHold], HoldList, SMNoteList):

    def _upcast(self, objList: List = None) -> SMHoldList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMHoldList
        """
        return SMHoldList(objList)

    def mult_offset(self, by: float, inplace:bool = False):
        HoldList.mult_offset(self, by=by, inplace=inplace)

    def data(self) -> List[SMHold]:
        return self

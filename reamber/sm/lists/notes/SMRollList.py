from __future__ import annotations

from typing import List

from reamber.base.lists.notes.HoldList import HoldList
from reamber.sm.SMRoll import SMRoll
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMRollList(List[SMRoll], HoldList, SMNoteList):

    def _upcast(self, objList: List = None) -> SMRollList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMRollList
        """
        return SMRollList(objList)

    def data(self) -> List[SMRoll]:
        return self

    def multOffset(self, by: float, inplace:bool = False):
        HoldList.multOffset(self, by=by, inplace=inplace)

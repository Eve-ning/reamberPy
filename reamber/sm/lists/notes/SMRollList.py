from __future__ import annotations

from typing import List

from reamber.base.lists.notes.HoldList import HoldList
from reamber.sm.SMRoll import SMRoll
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMRollList(List[SMRoll], HoldList, SMNoteList):

    def _upcast(self, obj_list: List = None) -> SMRollList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: SMRollList
        """
        return SMRollList(obj_list)

    def data(self) -> List[SMRoll]:
        return self


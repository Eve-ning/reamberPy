from __future__ import annotations

from typing import List

from reamber.base.lists.notes.HoldList import HoldList
from reamber.sm.SMHold import SMHold
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMHoldList(List[SMHold], HoldList, SMNoteList):

    def _upcast(self, obj_list: List = None) -> SMHoldList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: SMHoldList
        """
        return SMHoldList(obj_list)

    def data(self) -> List[SMHold]:
        return self

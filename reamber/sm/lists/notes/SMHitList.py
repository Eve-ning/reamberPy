from __future__ import annotations

from typing import List

from reamber.sm.SMHit import SMHit
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMHitList(List[SMHit], SMNoteList):

    def _upcast(self, obj_list: List = None) -> SMHitList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: SMHitList
        """
        return SMHitList(obj_list)

    def data(self) -> List[SMHit]:
        return self

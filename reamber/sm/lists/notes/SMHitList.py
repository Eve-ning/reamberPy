from __future__ import annotations

from typing import List

from reamber.sm.SMHit import SMHit
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMHitList(List[SMHit], SMNoteList):

    def _upcast(self, objList: List = None) -> SMHitList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMHitList
        """
        return SMHitList(objList)

    def data(self) -> List[SMHit]:
        return self

from __future__ import annotations

from typing import List

from reamber.dummy.DmHit import DmHit
from reamber.dummy.lists.notes.DmNoteList import DmNoteList


class DmHitList(List[DmHit], DmNoteList):

    def _upcast(self, objList: List = None) -> DmHitList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: DmHitList
        """
        return DmHitList(objList)

    def data(self) -> List[DmHit]:
        return self

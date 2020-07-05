from __future__ import annotations
from reamber.dummy.lists.notes.DmNoteList import DmNoteList
from reamber.dummy.DmHit import DmHit
from typing import List


class DmHitList(List[DmHit], DmNoteList):

    def _upcast(self, objList: List = None) -> DmHitList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: DmHitList
        """
        return DmHitList(objList)

    def data(self) -> List[DmHit]:
        return self

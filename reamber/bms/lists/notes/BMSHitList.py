from __future__ import annotations

from typing import List

from reamber.bms.BMSHit import BMSHit
from reamber.bms.lists.notes.BMSNoteList import BMSNoteList


class BMSHitList(List[BMSHit], BMSNoteList):

    def _upcast(self, objList: List = None) -> BMSHitList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: BMSHitList
        """
        return BMSHitList(objList)

    def data(self) -> List[BMSHit]:
        return self

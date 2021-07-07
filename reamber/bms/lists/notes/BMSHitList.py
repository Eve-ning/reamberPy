from __future__ import annotations

from typing import List

from reamber.bms.BMSHit import BMSHit
from reamber.bms.lists.notes.BMSNoteList import BMSNoteList


class BMSHitList(List[BMSHit], BMSNoteList):

    def _upcast(self, obj_list: List = None) -> BMSHitList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: BMSHitList
        """
        return BMSHitList(obj_list)

    def data(self) -> List[BMSHit]:
        return self

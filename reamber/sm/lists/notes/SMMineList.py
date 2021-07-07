from __future__ import annotations

from typing import List

from reamber.sm.SMMine import SMMine
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMMineList(List[SMMine], SMNoteList):

    def _upcast(self, obj_list: List = None) -> SMMineList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: SMMineList
        """
        return SMMineList(obj_list)

    def data(self) -> List[SMMine]:
        return self

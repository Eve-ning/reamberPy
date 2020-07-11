from __future__ import annotations

from typing import List

from reamber.sm.SMMine import SMMine
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMMineList(List[SMMine], SMNoteList):

    def _upcast(self, objList: List = None) -> SMMineList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMMineList
        """
        return SMMineList(objList)

    def data(self) -> List[SMMine]:
        return self

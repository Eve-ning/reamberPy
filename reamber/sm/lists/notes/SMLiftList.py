from __future__ import annotations
from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMLift import SMLift
from typing import List


class SMLiftList(List[SMLift], SMNoteList):

    def _upcast(self, objList: List = None) -> SMLiftList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMLiftList
        """
        return SMLiftList(objList)

    def data(self) -> List[SMLift]:
        return self

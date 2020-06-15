from __future__ import annotations
from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMLiftObj import SMLiftObj
from typing import List


class SMLiftList(List[SMLiftObj], SMNoteList):

    def _upcast(self, objList: List = None) -> SMLiftList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMLiftList
        """
        return SMLiftList(objList)

    def data(self) -> List[SMLiftObj]:
        return self

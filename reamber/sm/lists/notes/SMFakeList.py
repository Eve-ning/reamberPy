from __future__ import annotations

from typing import List

from reamber.sm.SMFake import SMFake
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMFakeList(List[SMFake], SMNoteList):

    def _upcast(self, objList: List = None) -> SMFakeList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMFakeList
        """
        return SMFakeList(objList)

    def data(self) -> List[SMFake]:
        return self

from __future__ import annotations
from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMKeySoundObj import SMKeySoundObj
from typing import List


class SMKeySoundList(List[SMKeySoundObj], SMNoteList):

    def _upcast(self, objList: List = None) -> SMKeySoundList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMKeySoundList
        """
        return SMKeySoundList(objList)

    def data(self) -> List[SMKeySoundObj]:
        return self

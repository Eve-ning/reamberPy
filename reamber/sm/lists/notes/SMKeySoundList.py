from __future__ import annotations
from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMKeySound import SMKeySound
from typing import List


class SMKeySoundList(List[SMKeySound], SMNoteList):

    def _upcast(self, objList: List = None) -> SMKeySoundList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMKeySoundList
        """
        return SMKeySoundList(objList)

    def data(self) -> List[SMKeySound]:
        return self

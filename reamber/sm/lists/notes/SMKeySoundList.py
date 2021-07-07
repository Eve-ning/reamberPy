from __future__ import annotations

from typing import List

from reamber.sm.SMKeySound import SMKeySound
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMKeySoundList(List[SMKeySound], SMNoteList):

    def _upcast(self, obj_list: List = None) -> SMKeySoundList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: SMKeySoundList
        """
        return SMKeySoundList(obj_list)

    def data(self) -> List[SMKeySound]:
        return self

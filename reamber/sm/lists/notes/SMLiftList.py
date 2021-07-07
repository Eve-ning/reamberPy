from __future__ import annotations

from typing import List

from reamber.sm.SMLift import SMLift
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMLiftList(List[SMLift], SMNoteList):

    def _upcast(self, obj_list: List = None) -> SMLiftList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: SMLiftList
        """
        return SMLiftList(obj_list)

    def data(self) -> List[SMLift]:
        return self

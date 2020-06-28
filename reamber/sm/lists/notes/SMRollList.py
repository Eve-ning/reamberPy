from __future__ import annotations
from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMRoll import SMRoll
from typing import List


class SMRollList(List[SMRoll], SMNoteList):

    def _upcast(self, objList: List = None) -> SMRollList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMRollList
        """
        return SMRollList(objList)

    def data(self) -> List[SMRoll]:
        return self

    # Copied from Holds, don't think it's worth splitting this further to just reduce repeated code
    def lengths(self) -> List[float]:
        return self.attribute('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attribute('tailOffset')]

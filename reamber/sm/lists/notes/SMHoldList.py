from __future__ import annotations
from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMHoldObj import SMHoldObj
from typing import List


class SMHoldList(List[SMHoldObj], SMNoteList):

    def _upcast(self, objList: List = None) -> SMHoldList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMHoldList
        """
        return SMHoldList(objList)

    def data(self) -> List[SMHoldObj]:
        return self

    def lengths(self) -> List[float]:
        return self.attribute('length')

    def offsets(self, flatten=True):
        if flatten: return [i for j in [(obj.offset, obj.tailOffset()) for obj in self.data()] for i in j]
        return [(obj.offset, obj.tailOffset()) for obj in self.data()]

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attribute('tailOffset')]

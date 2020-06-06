from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMHoldObj import SMHoldObj
from typing import List


class SMHoldList(List[SMHoldObj], SMNoteList):
    def data(self) -> List[SMHoldObj]:
        return self

    def lengths(self) -> List[float]:
        return self.attributes('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attributes('tailOffset')]

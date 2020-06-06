from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMHoldObject import SMHoldObject
from typing import List


class SMHoldList(List[SMHoldObject], SMNoteList):
    def data(self) -> List[SMHoldObject]:
        return self

    def lengths(self) -> List[float]:
        return self.attributes('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attributes('tailOffset')]

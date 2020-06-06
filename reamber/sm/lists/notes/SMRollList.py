from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMRollObject import SMRollObject
from typing import List


class SMRollList(List[SMRollObject], SMNoteList):
    def data(self) -> List[SMRollObject]:
        return self

    # Copied from Holds, don't think it's worth splitting this further to just reduce repeated code
    def lengths(self) -> List[float]:
        return self.attributes('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attributes('tailOffset')]

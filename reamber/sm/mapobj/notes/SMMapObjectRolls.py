from reamber.sm.mapobj.notes.SMMapObjectNoteBase import SMMapObjectNoteBase
from reamber.sm.SMRollObject import SMRollObject
from typing import List


class SMMapObjectRolls(List[SMRollObject], SMMapObjectNoteBase):
    def data(self) -> List[SMRollObject]:
        return self

    # Copied from Holds, don't think it's worth splitting this further to just reduce repeated code
    def lengths(self) -> List[float]:
        return self.attributes('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attributes('tailOffset')]

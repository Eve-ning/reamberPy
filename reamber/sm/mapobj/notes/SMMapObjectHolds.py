from reamber.sm.mapobj.notes.SMMapObjectNoteBase import SMMapObjectNoteBase
from reamber.sm.SMHoldObject import SMHoldObject
from typing import List


class SMMapObjectHolds(List[SMHoldObject], SMMapObjectNoteBase):
    def data(self) -> List[SMHoldObject]:
        return self

    def lengths(self) -> List[float]:
        return self.attributes('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attributes('tailOffset')]
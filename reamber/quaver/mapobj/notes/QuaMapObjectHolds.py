from reamber.quaver.mapobj.notes.QuaMapObjectNoteBase import QuaMapObjectNoteBase
from reamber.quaver.QuaHoldObject import QuaHoldObject
from typing import List


class QuaMapObjectHolds(List[QuaHoldObject], QuaMapObjectNoteBase):
    def data(self) -> List[QuaHoldObject]:
        return self

    def lengths(self) -> List[float]:
        return self.attributes('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attributes('tailOffset')]

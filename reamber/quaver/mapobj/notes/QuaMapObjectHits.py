from reamber.quaver.mapobj.notes.QuaMapObjectNoteBase import QuaMapObjectNoteBase
from reamber.quaver.QuaHitObject import QuaHitObject
from typing import List


class QuaMapObjectHits(List[QuaHitObject], QuaMapObjectNoteBase):
    def data(self) -> List[QuaHitObject]:
        return self

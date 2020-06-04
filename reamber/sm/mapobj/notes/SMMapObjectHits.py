from reamber.sm.mapobj.notes.SMMapObjectNoteBase import SMMapObjectNoteBase
from reamber.sm.SMHitObject import SMHitObject
from typing import List


class SMMapObjectHits(List[SMHitObject], SMMapObjectNoteBase):
    def data(self) -> List[SMHitObject]:
        return self

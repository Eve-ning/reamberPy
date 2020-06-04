from reamber.sm.mapobj.notes.SMMapObjectNoteBase import SMMapObjectNoteBase
from reamber.sm.SMLiftObject import SMLiftObject
from typing import List


class SMMapObjectLifts(List[SMLiftObject], SMMapObjectNoteBase):
    def data(self) -> List[SMLiftObject]:
        return self

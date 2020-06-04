from reamber.sm.mapobj.notes.SMMapObjectNoteBase import SMMapObjectNoteBase
from reamber.sm.SMKeySoundObject import SMKeySoundObject
from typing import List


class SMMapObjectKeySounds(List[SMKeySoundObject], SMMapObjectNoteBase):
    def data(self) -> List[SMKeySoundObject]:
        return self

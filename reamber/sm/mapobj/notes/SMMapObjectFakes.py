from reamber.sm.mapobj.notes.SMMapObjectNoteBase import SMMapObjectNoteBase
from reamber.sm.SMFakeObject import SMFakeObject
from typing import List


class SMMapObjectFakes(List[SMFakeObject], SMMapObjectNoteBase):
    def data(self) -> List[SMFakeObject]:
        return self

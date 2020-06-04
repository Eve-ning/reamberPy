from reamber.sm.mapobj.notes.SMMapObjectNoteBase import SMMapObjectNoteBase
from reamber.sm.SMMineObject import SMMineObject
from typing import List


class SMMapObjectMines(List[SMMineObject], SMMapObjectNoteBase):
    def data(self) -> List[SMMineObject]:
        return self
